import json
from typing import Type
import os
from datetime import datetime

battle_log_file="powerPlay\\battlelogs\\battlelogs_20210926-151835_global.json"
battlelogsDirectory = r'powerPlay\\battlelogs'
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

def get_curent_player_tag(itemNumber, battle_log_file):
    tags_file="powerPlay\\tags\\tags"+battle_log_file.split("\\")[-1].split("battlelogs")[-1]
    file = open(tags_file)
    content = file.readlines()
    curentPlayer=content[itemNumber-1].rstrip("\n")
    return curentPlayer

def get_team_of_star_player_from_tags(item, itemNumber, battle_log_file):
    curentPlayer=get_curent_player_tag(itemNumber, battle_log_file)
    curentPlayerSeen=False
    goodTeam=False
    winTeam=[]
    result=item["battle"]["result"]
    teams= item["battle"]["teams"]
    for team in teams:
            winTeam.clear()
            for i in range(len(team)):
                winTeam.append(team[i]["brawler"]["name"])
                if team[i]["tag"]==curentPlayer:
                    if result=="victory":
                        goodTeam=True
                        curentPlayerSeen=True
                    else:
                        curentPlayerSeen=True
                        goodTeam=False
            if goodTeam:
                break
            if result!="victory" and curentPlayerSeen==False:
                break

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

# Store an item to the merged battlelogs file
def store_item(item, itemNumber, filename, dt_string):
    currentPlayerTag= get_curent_player_tag(itemNumber, filename)
    item["PlayerTag"]=currentPlayerTag
    if(os.path.isfile(dt_string)):
        data = json.load(open(dt_string))
        # convert data to list if not
        if type(data) is dict:
            data = [data]

        # append new item to data lit
        data.append(item)

        # write list to file
        with open(dt_string, 'w') as outfile:
            json.dump(data, outfile, indent=4)
    else:
        with open(dt_string, 'w') as outfile:
            json.dump(item, outfile, indent=4)


now = datetime.now()
dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")

for fileName in os.listdir(battlelogsDirectory): # For all files of powerPLay/batttlelogs directory
    filename=os.path.join(battlelogsDirectory, fileName)
    with open(filename) as f:
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
    itemNumber=0
    noModeInEvent=0 # Certainly championship!
    notFound=0
    for data in datas: # For each player
        itemNumber=itemNumber+1
        if "items" in data: # Check if there is no problem like the 148
            for item in data['items']: # For each batle of the battlelogs of the curent player
                if "mode" in item['event']: # Check if there is a mode or not
                    if get_mode_from_item(item)=="gemGrab": # if we are in gemgrab mode
                        if item["battle"]["type"] == "soloRanked" or item["battle"]["type"] == "teamRanked": # if we are in power league
                            powerLeagueMap= get_map_from_item(item)
                            powerLeagueWinTeam= get_team_of_star_player_from_tags(item, itemNumber, filename)
                            powerLeagueWinTable= store_winning_teams_per_map(powerLeagueMap, powerLeagueWinTeam, powerLeagueWinTable)
                        if item["battle"]["type"] != "soloRanked":     
                            if item["battle"]["type"] != "teamRanked": # If we are not in power league
                                if get_map_from_item(item)!= None: # Check if the map is not null
                                    map= get_map_from_item(item)
                                    winTeam= get_team_of_star_player_from_tags(item, itemNumber, filename)
                                    winTable= store_winning_teams_per_map(map, winTeam, winTable)
                                else:
                                    nullMap=nullMap+1
                            else: # if we are in team ranked power league
                                teamRanked=teamRanked+1
                                teamRankedMap= get_map_from_item(item)
                                teamRankedWinTeam= get_team_of_star_player_from_tags(item, itemNumber, filename)
                                teamRankedWinTable= store_winning_teams_per_map(teamRankedMap, teamRankedWinTeam, teamRankedWinTable)                                
                                if powerLeagueMap=="Hard Rock Mine":
                                    teamHardRock=teamHardRock+1
                                    store_item(item, itemNumber, filename,os.path.join("powerPlay\\battlelogsMerge","team_ranked_merged_battlelogs_hard_rock_mine_"+dt_string+".json"))                        
                        else: # if we are in solo ranked power league
                            soloRanked=soloRanked+1
                            soloRankedMap= get_map_from_item(item)
                            soloRankedWinTeam= get_team_of_star_player_from_tags(item, itemNumber, filename)
                            soloRankedWinTable= store_winning_teams_per_map(soloRankedMap, soloRankedWinTeam, soloRankedWinTable)
                            if powerLeagueMap=="Hard Rock Mine":
                                soloHardRock=soloHardRock+1
                                store_item(item, itemNumber, filename,os.path.join("powerPlay\\battlelogsMerge","solo_ranked_merged_battlelogs_hard_rock_mine_"+dt_string+".json"))

                else:
                    noModeInEvent=noModeInEvent+1
        else:
            notFound=notFound+1


    winTable =sort_win_table(winTable)
    #print_win_table(winTable)

    print("power league")
    powerLeagueWinTable =sort_win_table(powerLeagueWinTable)
    print_win_table(powerLeagueWinTable)

    print("solo ranked")
    soloRankedWinTable =sort_win_table(soloRankedWinTable)
    #print_win_table(soloRankedWinTable)

    print("team ranked")
    teamRankedWinTable =sort_win_table(teamRankedWinTable)
    #print_win_table(teamRankedWinTable)

    print("solo hard rock: ", soloHardRock)
    print("team hard rock: ", teamHardRock)