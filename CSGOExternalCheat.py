
from Feature import Feature
import pymem
import pymem.process
import requests
import threading
import keyboard
import sys

from Menu import Menu

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

# input process name
nameprocess = "csgo.exe"

pm=pymem.Pymem(nameprocess)

client = pymem.process.module_from_name( pm.process_handle, "client.dll" ).lpBaseOfDll
engine = pymem.process.module_from_name( pm.process_handle, "engine.dll" ).lpBaseOfDll

def thread_func():
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

def RadarHack():
    while True:
        for i in range(32):
            entity=pm.read_int(client + dwEntityList + i * 0x10)
            if entity:
                pm.write_uchar(entity+m_bSpotted,1)

def rankReveal():
    playerResource=pm.read_int(client+dwPlayerResource)
    radarBase=pm.read_int(client+dwRadarBase)
    radarPTR=pm.read_int(radarBase+0x78)
    for i in range(2,32):
        name=pm.read_string(radarPTR + 0x300+ (0x174 * (i-1)),32)
        ranks=pm.read_int(playerResource+m_iCompetitiveRanking+ (i * 0x04))
        wins=pm.read_int(playerResource+m_iCompetitiveWins+ (i * 0x04))
        if name:
            print(name)
            print("Ranks:  {}, Wins: {}".format(Ranks[ranks],wins))

if __name__=="__main__":
    arr=[
        Feature("Anti-Flash",thread_func),
        Feature("Glow",glow),
        Feature("Radar Hack",RadarHack),
    ]

    UI=Menu(arr)
    UI.displayMenu()

    print("------------------ Rank Reveal -----------------")
    rankReveal()
    print("------------------------------------------------")
    
    # hop=threading.Thread(target=bhop)
    # hop.start()
    # hop=threading.Thread(target=enemyHealth)
    # hop.start()
