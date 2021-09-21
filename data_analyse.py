import json

battle_log_file="battlelogs\\battlelogs_20210905-125408.json"

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



with open(battle_log_file) as f:
    datas = json.load(f)
winTable={}
soloRanked=0
teamRanked=0
nullMap=0
noModeInEvent=0 # Certainly power league or championship!
notFound=0
for data in datas:
    if "items" in data:
        for item in data['items']:
            print(item["battleTime"])
            if "mode" in item['event']:
                if get_mode_from_item(item)=="brawlBall":
                    if item["battle"]["type"] != "soloRanked":
                        if item["battle"]["type"] != "teamRanked":
                            if get_map_from_item(item)!= None:
                                map= get_map_from_item(item)
                                winTeam= get_team_of_star_player(item)
                                store_winning_teams_per_map(map, winTeam, winTable)
                            else:
                                nullMap=nullMap+1
                        else:
                            teamRanked=teamRanked+1
                    else:
                        soloRanked=soloRanked+1
            else:
                noModeInEvent=noModeInEvent+1
    else:
        notFound=notFound+1

print("Table: ")
for item in winTable:
    print(item)
    for keys in winTable[item]:
        print(keys, ':', winTable[item][keys])
print("")
