
import pymem
import pymem.process
import requests
import threading

Ranks=[
        "Unranked",

        "Silver I",
        "Silver II",
        "Silver III",
        "Silver IV",
        "Silver Elite",
        "Silver Elite Master",

        "Gold Nova I",
        "Gold Nova II",
        "Gold Nova III",
        "Gold Nova Master",
        "Master Guardian I",
        "Master Guardian II",

        "Master Guardian Elite",
        "Distinguished Master Guardian",
        "Legendary Eagle",
        "Legendary Eagle Master",
        "Supreme Master First Class",
        "The Global Elite"
]
offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get( offsets ).json()
m_iAccountID=12232
m_iCompetitiveWins = int(response["netvars"]["m_iCompetitiveWins"])
dwEntityList = int( response["signatures"]["dwEntityList"] )
dwGlowObjectManager = int( response["signatures"]["dwGlowObjectManager"] )
m_iGlowIndex = int( response["netvars"]["m_iGlowIndex"] )
m_iTeamNum = int( response["netvars"]["m_iTeamNum"] )
dwForceJump =int( response["signatures"]["dwForceJump"] )
dwLocalPlayer = int( response["signatures"]["dwLocalPlayer"] )
dwRadarBase=int( response["signatures"]["dwRadarBase"] )
m_fFlags = int( response["netvars"]["m_fFlags"] )
dwForceAttack = int( response["signatures"]["dwForceAttack"] )
m_iCrosshairId = int( response["netvars"]["m_iCrosshairId"] )
m_flFlashMaxAlpha = int( response["netvars"]["m_flFlashMaxAlpha"] )
m_iDefaultFOV = (0x332C)
dwClientState = response["signatures"]["dwClientState"]
m_iHealth =(0x100)
dwViewMatrix = int( response["signatures"]["dwViewMatrix"] )
m_dwBoneMatrix = int( response["netvars"]["m_dwBoneMatrix"] )
dwClientState_ViewAngles = int( response["signatures"]["dwClientState_ViewAngles"] )
m_vecOrigin = int( response["netvars"]["m_vecOrigin"] )
m_vecViewOffset = int( response["netvars"]["m_vecViewOffset"] )
dwbSendPackets = int( response["signatures"]["dwbSendPackets"] )
dwInput = int( response["signatures"]["dwInput"] )
clientstate_net_channel = int( response["signatures"]["clientstate_net_channel"] )
clientstate_last_outgoing_command = int( response["signatures"]["clientstate_last_outgoing_command"] )
m_bSpotted = int( response["netvars"]["m_bSpotted"] )
m_iShotsFired = int( response["netvars"]["m_iShotsFired"] )
m_aimPunchAngle = int( response["netvars"]["m_aimPunchAngle"])
m_bGunGameImmunity = int( response["netvars"]["m_bGunGameImmunity"] )
m_bIsDefusing = int( response["netvars"]["m_bIsDefusing"] )
m_bDormant = int( response["signatures"]["m_bDormant"] )
dwClientState_PlayerInfo = int( response["signatures"]["dwClientState_PlayerInfo"] )
dwPlayerResource = int( response["signatures"]["dwPlayerResource"] )
m_iCompetitiveRanking = int( response["netvars"]["m_iCompetitiveRanking"] )
m_szCustomName=int( response["netvars"]["m_szCustomName"] )
# input process name
nameprocess = "csgo.exe"

pm=pymem.Pymem(nameprocess)

client = pymem.process.module_from_name( pm.process_handle, "client.dll" ).lpBaseOfDll
engine = pymem.process.module_from_name( pm.process_handle, "engine.dll" ).lpBaseOfDll

def thread_func():
    print("Start")
    player = pm.read_int(client+dwLocalPlayer)
    while True:

        if player:
            value=player+m_flFlashMaxAlpha
            if value:
                pm.write_float(player+m_flFlashMaxAlpha,float(0))
            else:
                pass

def glow():
    while True:
        glow_manager = pm.read_int(client+dwGlowObjectManager)
        for i in range(1,32):
            entity=pm.read_int(client+dwEntityList+i*0x10)

            if entity>0:
                entity_team_id=pm.read_int(entity+m_iTeamNum)
                entity_glow=pm.read_int(entity+m_iGlowIndex)
            
                if entity_team_id==2:
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)          # Enable glow

                elif entity_team_id==3:
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)           # Enable glow

def rank():
    playerResource=pm.read_int(client+dwPlayerResource)
    for i in range(1,32):
        ranks=pm.read_int(playerResource+m_iCompetitiveRanking+ (i * 0x04))
        wins=pm.read_int(playerResource+m_iCompetitiveWins+ (i * 0x04))
        if wins!=0:
            print("Ranks:  {}, Wins: {}".format(Ranks[ranks],wins))
        #name=pm.read_int(playerResource+m_iCompetitiveRanking+ (i * 0x04))
        #print(pm.read_string(radarptr+ + 0x300 + (0x174 * i)))
        #print(pm.read_int(playerResource+m_iTeamNum + (i * 0x10)))


def name():
    for i in range(1,32):
        player_info = pm.read_int(client+dwClientState +dwClientState_PlayerInfo)
        player_info_items = pm.read_int(pm.read_int(player_info + 0x40) + 0xC)
        info = pm.read_int(player_info_items + 0x28 + ((i-1) * 0x34))
        print(pm.read_string(info + 0x10))
    #C.get('dwClientState_PlayerInfo') = dwClientState_PlayerInfo in hazedumper
    #nickname pm.read_string(info + 0x10)
    #steamid pm.read_string(info + 0x94)

    # print(client)
    # print(dwRadarBase)
    # print(dwLocalPlayer)
    # print(client +dwRadarBase)
    # radar_base = pm.read_int(client +dwRadarBase)
    # c_hud_radar = pm.read_int(radar_base + 0x74)
    # #entity=pm.read_int(client+dwEntityList+i*0x10)
    # for i in range(1,32):
    #     name = pm.read_string(c_hud_radar + 0x300 + (0x174 * i))
    #     print(name)

def GetPlayers():
    player_addrs = []
    for i in range(64):
        player_addr_ = pm.read_int(client + dwEntityList + 0x10*i)
        if player_addr_ == 0x0: continue
        player_addrs.append(player_addr_)
        print(pm.read_int(player_addr_+m_iHealth))
        #print(pm.read_int(player_addr_+m_szCustomName))
    return player_addrs

def GetId(addr):
    vt = pm.read_int(addr + 0x8)
    fn = pm.read_int(vt + 2 * 0x4)
    cls = pm.read_int(fn + 0x1)
    clsn = pm.read_int(cls + 8)
    return pm.read_string(clsn + 20)    
if __name__=="__main__":
    
    # antiflash=threading.Thread(target=thread_func)
    # antiflash.start() 
    # glowThread=threading.Thread(target=glow)
    # glowThread.start()
    rank()
    