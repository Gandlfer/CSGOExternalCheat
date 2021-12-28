
import pymem
import pymem.process
import requests
import threading
import keyboard

offsets = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get( offsets ).json()
bhop_taste = "space"
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

def bhop():
    while True:
        # if keyboard.is_pressed("end"):
        #     pass
        if keyboard.is_pressed("space"):
            print("Pressed")
            jmp= client+dwForceJump
            player = pm.read_int(client+dwLocalPlayer)
            on_ground=pm.read_int(player+m_fFlags)
            if player and jmp and on_ground==257:
                pm.write_int(jmp,6)
            else:
                pass

    
def enemyHealth():
    
    while True:
        if keyboard.is_pressed("alt"):
            radar = pm.read_int( client + dwRadarBase)
            c_hud_radar = pm.read_int(radar + 0x74)
            #name= pm.read_string(c_hud_radar + 0x300 + (0x174 * ( - 1))
            #print(name)
            # name= pm.read_string(c_hud_radar + 0x18 + (0x174 * 2))
            # print(name)
            for i in range(1,64):
                name = pm.read_string(c_hud_radar + 0x300 + 0x174 * i )
                print("{} \n {}".format(i,name))
                #if enemyTeam:

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

def RadarHack():
    while True:
        if pm.read_int(client + dwLocalPlayer):
            localplayer = pm.read_int(client + dwLocalPlayer)
            localplayer_team = pm.read_int(localplayer + m_iTeamNum)
            for i in range(64):
                if pm.read_int(client + dwEntityList + i * 0x10):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    entity_team = pm.read_int(entity + m_iTeamNum)
                    if entity_team != localplayer_team:
                        pm.write_int(entity + m_bSpotted, 1)

if __name__=="__main__":

    # antiflash=threading.Thread(target=thread_func)
    # antiflash.start()
    glowThread=threading.Thread(target=glow)
    glowThread.start()

    #threading.Thread(target=RadarHack).start()
    # hop=threading.Thread(target=bhop)
    # hop.start()
    # hop=threading.Thread(target=enemyHealth)
    # hop.start()
