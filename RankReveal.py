from re import L
import pymem
import pymem.process
import requests

offsets = "https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json"
response = requests.get(offsets).json()
m_iCompetitiveWins = int(response["netvars"]["m_iCompetitiveWins"])
dwEntityList = int(response["signatures"]["dwEntityList"])
m_iTeamNum = int(response["netvars"]["m_iTeamNum"])
dwRadarBase = int(response["signatures"]["dwRadarBase"])
dwPlayerResource = int(response["signatures"]["dwPlayerResource"])
m_iCompetitiveRanking = int(response["netvars"]["m_iCompetitiveRanking"])
Ranks = [
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
    "The Global Elite",
]

# input process name
nameprocess = "csgo.exe"

pm = pymem.Pymem(nameprocess)

client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll


def rankReveal():
    lobby = dict()
    lobby[2] = list()
    lobby[3] = list()
    lobby[0] = list()
    playerResource = pm.read_int(client + dwPlayerResource)
    radarBase = pm.read_int(client + dwRadarBase)
    radarPTR = pm.read_int(radarBase + 0x78)
    for i in range(2, 32):
        entity = pm.read_int(client + dwEntityList + (i - 1) * 0x10)
        if entity > 0:
            name = pm.read_string(radarPTR + 0x300 + (0x174 * (i - 1)), 33)
            x = str(20 - len(name))
            ranks = pm.read_int(playerResource + m_iCompetitiveRanking + (i * 0x04))
            wins = pm.read_int(playerResource + m_iCompetitiveWins + (i * 0x04))
            lobby[pm.read_int(entity + m_iTeamNum)].append(
                "Player: {:<40} Ranks: {}, Wins: {}".format(name, Ranks[ranks], wins)
            )

    print("Terrorist {: >10}".format(len(lobby[2])))
    for x in lobby[2]:
        print(x)
    print("-" * 50)
    print("Counter Terrorist {: >10}".format(len(lobby[3])))
    for x in lobby[3]:
        print(x)


if __name__ == "__main__":
    rankReveal()
    k = input("Enter anything to close...")
