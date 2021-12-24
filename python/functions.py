import json
import requests
from battle import Battle 
from datetime import datetime
import os
from pathlib import Path
from collections import Counter

def READ_API_TOKEN(filepath):
    """
    Desc:	Read the API token from a file
    Input:	String: filename
    Output: String: API token
    """
    infile = open(filepath, 'r')
    data = infile.read()
    infile.close()
    return data.strip()

def GET_PLAYER_STATS(token, tag):
    headers = {'Authorization':'Bearer '+token}
    data={}
    #url_tag="%23"+tag
    url_tag=tag.replace("#","%23")
    response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=data)
    battlelogs = response.json()
    return battlelogs

def GET_CURRENT_EVENTS(token):
    headers = {'Authorization':'Bearer '+token}
    data={}
    response = requests.request("GET", "https://api.brawlstars.com/v1/events/rotation", headers=headers, data=data)
    current_events = response.json()
    with open('../data/events/current_events.json', 'w') as f:
        json.dump(current_events, f)
    return

def READ_CURRENT_EVENTS(filepath):
    with open('../data/events/current_events.json') as f:
        current_events=json.load(f)
    return current_events

def READ_EVENTS_STATS(mode,map):
    with open('../data/stats/'+mode+'_'+map+'.json') as f:
        events_stats=json.load(f)
    return events_stats

def GET_RANKINGS(token,countries_list,player_limit):
    """
    Desc:   GET tags of leaderboard
    Input:  API token
    Output: A 200 player json file
    """
    ranks_list={}
    headers = {'Authorization':'Bearer '+token}
    data={}
    for country in countries_list:
        url = "https://api.brawlstars.com/v1/rankings/"+country+"/players?limit="+str(player_limit)
        response = requests.request("GET", url, headers=headers, data=data)
        ranks_list[country]=response.json()
        print("Country:" + country + ", Response code: " + str(response.status_code))
    return ranks_list

def GET_BATTLELOGS(token, ranks_list):
    """
    Desc:   GET battlelogs from tag list
    Input:  A list of tags
    Output: A battlelogs json file of the tags in input
    """
    battlelogs_list={}
    battlelogs={}
    headers = {'Authorization': 'Bearer '+token}
    data = {}
    for country in ranks_list:
        for player in ranks_list[country]['items']:
            tag=player["tag"]
            url_tag=tag.replace("#","%23")
            response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=data)
            battlelogs[tag]= response.json()
            print("Country:" + country + ", Tag: "+ tag + ", Response code: " + str(response.status_code))
        battlelogs_list[country]=battlelogs
    return battlelogs_list

def EXTRACT_TEAM_RESULT(battle):
    """
    Desc:   RETURN SORTED WIN AND LOSE TEAM BASED ON BATTLE
    """

    #FIND INDEX WIN AND LOSE TEAM
    winTeamIndex=1
    loseTeamIndex=0
    for game_player in battle["battle"]["teams"][0]:
        if (str(battle["battle"]["starPlayer"]["tag"]) == str(game_player["tag"])):
            winTeamIndex=0
            loseTeamIndex=1

    #COLLECT BRAWLERS IN EACH TEAM
    winTeam=[]
    loseTeam=[]
    for brawler in battle["battle"]["teams"][winTeamIndex]:
        winTeam.append(brawler["brawler"]["name"])
    for brawler in battle["battle"]["teams"][loseTeamIndex]:
        loseTeam.append(brawler["brawler"]["name"])
    
    #SORT AND RETURN TEAMS
    winTeam=sorted(winTeam)
    loseTeam=sorted(loseTeam)
    return winTeam, loseTeam

def COMPUTE_BEST_BRAWLER(mode,map, startTime):
    mode="gemGrab"
    map="Four Squared"
    startTime="20212212"

    #READ BATTLES
    with open('../data/battles/'+mode+"/"+map+"/"+startTime+"_"+mode+"_"+map+".json", 'r') as f:
        battles_mode_map = json.load(f)
    for battle in battles_mode_map:
        winTeam, loseTeam = EXTRACT_TEAM_RESULT(battle)

def unique_counter(filesets):
    for i in filesets:
        i['count'] = sum([1 for j in filesets if j['num'] == i['num']])
    return {k['num']:k for k in filesets}.values()

def remove_team_duplicate(team):
	team_no_dupplicate=[]
	for elem in team:
		if elem not in team_no_dupplicate:
			team_no_dupplicate.append(elem)
	return team_no_dupplicate

def STORE_BEST_TEAM(mode,map, startTime):
    mode="gemGrab"
    map="Four Squared"
    startTime="20211222T080000"
    winTeams=[]
    loseTeams=[]

    #READ BATTLES
    with open("../data/battles/"+mode+"/"+map+"/"+startTime+"_"+mode+"_"+map+".json", 'r') as f:
        battles_mode_map = json.load(f)

    #GET WIN AND LOSE TEAMS
    for battle in battles_mode_map:
        winTeam, loseTeam = EXTRACT_TEAM_RESULT(battle)
        winTeams.append(winTeam)
        loseTeams.append(loseTeam)
    
    winTeamsUnique=[]
    winTeamsUnique=remove_team_duplicate(winTeams)
    loseTeamsUnique=[]
    loseTeamsUnique=remove_team_duplicate(loseTeams)

    winTable=[]

    for team in winTeamsUnique:
        pickNumber=winTeams.count(team)+loseTeams.count(team)
        if(loseTeamsUnique.count(team)==0):
            winRate=1
        else:
            winRate=winTeams.count(team)/pickNumber
        win_dict = {
            "mode": mode,
            "map": map,
            "startTime": startTime, #start day
            "teamStats": {
                "winNumber": winTeams.count(team),
                "winRate":winRate,
                "pickRate": (winTeams.count(team)+loseTeams.count(team))/(len(battles_mode_map)),
                "pickNumber":pickNumber,
                "brawlers": team
                }
        }
        winTable.append(win_dict)
    filename = "../data/stats/gemGrab_Deathcap Trap.json"
    with open(filename, 'w') as fp:
	    json.dump(winTable, fp, indent=4)

    

def STORE_BATTLES(battlelogsList):
    now = datetime.now()
    dtString = now.strftime("%d_%m_%Y__%H_%M_%S")
    dataFolder = Path("Database")
    dataFolder.mkdir(parents=True, exist_ok=True)
    for pays in battlelogsList:
        for players in battlelogsList[pays]:
            for battles in battlelogsList[pays][players]["items"]:
                print(battles)
                b = Battle(battles)
                if not b.noDuration and not b.noResult and not b.noStarPlayer:
                    modeFolder= dataFolder/b.mode
                    modeFolder.mkdir(parents=True, exist_ok=True)
                    fileName=b.mapEvent+"_"+dtString+".json"
                    mapFile=modeFolder/fileName
                    if mapFile.is_file():
                        data = json.load(open(mapFile))
                        # convert data to list if not
                        if type(data) is dict:
                            data = [data]
                        alreadyExist=False
                        for batailles in data:
                            savedB=Battle(batailles)
                            if savedB.is_equal(b):
                                alreadyExist=True

                        if not alreadyExist:
                            # append new item to data lit
                            data.append(battles)

                            # write list to file
                            with open(mapFile, 'w') as outfile:
                                json.dump(data, outfile, indent=4)
                    else:
                        with open(mapFile, 'w') as outfile:
                            json.dump(battles, outfile, indent=4)