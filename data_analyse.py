import json
from typing import Type

battle_log_file="powerPlay\\battlelogs\\battlelogs_20210926-151835_global.json"

# INPUT   : An item from the json battle log with the following keys: "battle", "battleTime" and "event"
#           The map name shall be a key of the value of "event" 
# OUTPUT  : The sring of the map
# PROCESS : item-->event-->map-->stringName
def get_map_from_item(item):
    return item['event']["map"]

# INPUT   : An item from the json battle log with the following keys: "battle", "battleTime" and "event"
#           The map name shall be a key of the value of "event" 
# OUTPUT  : The sring of the mode
# PROCESS : item-->event-->mode-->stringName
def get_mode_from_item(item):
    return item['event']["mode"]

# INPUT   : An item from the json battle log with the following keys: "battle", "battleTime" and "event"
#           The map name shall be a key of the value of "event" 
# OUTPUT  : The tag of the star player
# PROCESS : item-->battle-->starPlayer-->tag-->stringTag
def get_star_player_from_item(item):
    if item["battle"]["starPlayer"]["tag"]==None:
        print("No star player")
    return item["battle"]["starPlayer"]["tag"]

# INPUT   : An item from the json battle log with the following keys: "battle", "battleTime" and "event"
#           The map name shall be a key of the value of "event" 
# OUTPUT  : A list of the winnig team
# PROCESS : - Get star player
#           - Search the team of the star player
#           - Return the winning team
def get_team_of_star_player(item):
    star=get_star_player_from_item(item)
    #25 battles
    goodTeam=False
    winTeam=[]

    teams= item["battle"]["teams"]
    for team in teams:
        if goodTeam== False:
            winTeam.clear()
            for i in range(len(team)):
                winTeam.append(team[i]["brawler"]["name"])
                if team[i]["tag"]==star:
                    goodTeam=True
    winTeam.sort()
    return winTeam


def store_winning_teams_per_map(map, winTeam, winTable):
    if map in winTable.keys():
        teamAlreadyExist=False
        for team in winTable[map]:
            if team == str(winTeam):
                winTable[map][team]= winTable[map][team]+1
                teamAlreadyExist=True
                break
        if teamAlreadyExist== False:
            winTable[map][str(winTeam)]=1
    else:
        teams={}
        teams[str(winTeam)]=1
        winTable[map]=teams
    return winTable

def sort_win_table(winTable):
    for map in winTable:
        sortedWinTable = dict(sorted(winTable[map].items(), key=lambda x: x[1], reverse=True))
        #{k: v for k, v in sorted(winTable[map].items(), key=lambda item: item[1], reverse=True)}
        winTable[map]=sortedWinTable
    return winTable

def print_win_table(winTable):
    for item in winTable:
        print(item)
        for keys in winTable[item]:
            print("\t", keys, ':', winTable[item][keys])
    print("")

with open(battle_log_file) as f:
    datas = json.load(f)
winTable={}
teamRankedWinTable={}
soloRankedWinTable={}
powerLeagueWinTable={}
soloHardRock=0
teamHardRock=0
soloRanked=0
teamRanked=0
nullMap=0
noModeInEvent=0 # Certainly power league or championship!
notFound=0
for data in datas:
    if "items" in data:
        for item in data['items']:
            if "mode" in item['event']:
                if get_mode_from_item(item)=="gemGrab":
                    if item["battle"]["type"] == "soloRanked" or item["battle"]["type"] == "teamRanked":
                        try: 
                            powerLeagueMap= get_map_from_item(item)
                            powerLeagueWinTeam= get_team_of_star_player(item)
                            powerLeagueWinTable= store_winning_teams_per_map(powerLeagueMap, powerLeagueWinTeam, powerLeagueWinTable)
                        except TypeError:
                            print("Power league: ", item["battleTime"])
                    if item["battle"]["type"] != "soloRanked":
                        if item["battle"]["type"] != "teamRanked":
                            if get_map_from_item(item)!= None:
                                map= get_map_from_item(item)
                                winTeam= get_team_of_star_player(item)
                                winTable= store_winning_teams_per_map(map, winTeam, winTable)
                            else:
                                nullMap=nullMap+1
                        else:
                            teamRanked=teamRanked+1
                            try: 
                                teamRankedMap= get_map_from_item(item)
                                teamRankedWinTeam= get_team_of_star_player(item)
                                teamRankedWinTable= store_winning_teams_per_map(teamRankedMap, teamRankedWinTeam, teamRankedWinTable)                                
                                if powerLeagueMap=="Hard Rock Mine":
                                    teamHardRock=teamHardRock+1
                            except TypeError:
                                print("Team ranked: ", item["battleTime"])
                    else:
                        soloRanked=soloRanked+1
                        try :
                            soloRankedMap= get_map_from_item(item)
                            soloRankedWinTeam= get_team_of_star_player(item)
                            soloRankedWinTable= store_winning_teams_per_map(soloRankedMap, soloRankedWinTeam, soloRankedWinTable)
                            if powerLeagueMap=="Hard Rock Mine":
                                soloHardRock=soloHardRock+1
                        except TypeError:
                            print("Solo ranked: ", item["battleTime"])
            else:
                noModeInEvent=noModeInEvent+1
    else:
        notFound=notFound+1

print_win_table(winTable)
winTable =sort_win_table(winTable)
print_win_table(winTable)

print("power league")
powerLeagueWinTable =sort_win_table(powerLeagueWinTable)
print_win_table(powerLeagueWinTable)

print("solo ranked")
soloRankedWinTable =sort_win_table(soloRankedWinTable)
print_win_table(soloRankedWinTable)

print("team ranked")
teamRankedWinTable =sort_win_table(teamRankedWinTable)
print_win_table(teamRankedWinTable)

print("solo hard rock: ", soloHardRock)
print("team hard rock: ", teamHardRock)