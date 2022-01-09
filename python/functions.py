import json
import requests
from battle import Battle 
from datetime import datetime
import os
from pathlib import Path
from collections import Counter
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import platform

if(platform.system()=="Windows"):
    path_separator="\\"
else:
    path_separator="/"


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

def READ_EVENTS_STATS(mode,map, startTime, soloOrTeams):
    if soloOrTeams=="teams":
        with open('../data/stats/teams/'+startTime+'_'+mode+'_'+map+'.json') as f:
            events_stats=json.load(f)
        return events_stats["teams"], events_stats["battlesNumber"]
    else:
        with open('../data/stats/solo/'+startTime+'_'+mode+'_'+map+'.json') as f:
            events_stats=json.load(f)
        return events_stats["brawler"], events_stats["battlesNumber"]


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

def GET_BATTLELOGS_backup(token, ranks_list):
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
        battlelogs.clear()
        for player in ranks_list[country]['items']:
            tag=player["tag"]
            url_tag=tag.replace("#","%23")
            response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=data)
            battlelogs[tag]= response.json()
            print("Country:" + country + ", Tag: "+ tag + ", Response code: " + str(response.status_code))
        battlelogs_list[country]=battlelogs
    return battlelogs_list

def GET_BATTLELOGS(token, ranks_list):
    """
    Desc:   GET battlelogs from tag list
    Input:  A list of tags
    Output: A battlelogs json file of the tags in input
    """
    battlelogs_list={}
    battlelogs={}
    threads= []
    with ThreadPoolExecutor(max_workers=40) as executor:

        for country in ranks_list:
            battlelogs.clear()
            threads.append(executor.submit(GET_BATTELOGS_API_CALLS, country, ranks_list, battlelogs, token))
            
        for task in as_completed(threads):
            print("API CALLS FINISH") 

        battlelogs_list[country]=battlelogs
    return battlelogs_list

def GET_BATTELOGS_API_CALLS(country, ranks_list, battlelogs, token):
    headers = {'Authorization': 'Bearer '+token}
    data = {}
    for player in ranks_list[country]['items']:
        tag=player["tag"]
        url_tag=tag.replace("#","%23")
        response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=data)
        battlelog=response.json()
        
        for battle in battlelog["items"]:
            battle["playerTag"]=tag #add the tag of the corresponding player in order to handle showdown
      
        battlelogs[tag]= battlelog
        print("Country:" + country + ", Tag: "+ tag + ", Response code: " + str(response.status_code))
    return battlelogs


def EXTRACT_TEAM_RESULT(battle):
    """
    Desc:   RETURN SORTED WIN AND LOSE TEAM BASED ON BATTLE
    """
    winTeam=[]
    loseTeam=[]

    b = Battle(battle)
    if b.mode== "duoShowdown":
        if b.rank <=2:
            for brawler in b.get_team_of_player():
                winTeam.append(brawler["brawler"]["name"])
        else:
            for brawler in b.get_team_of_player():
                loseTeam.append(brawler["brawler"]["name"])
    elif b.mode != "soloShowdown":
        #FIND INDEX WIN AND LOSE TEAM
        winTeamIndex=1
        loseTeamIndex=0
        for game_player in b.teams[0]:
            if (str(b.starTag) == str(game_player["tag"])):
                winTeamIndex=0
                loseTeamIndex=1

        #COLLECT BRAWLERS IN EACH TEAM
        
        for brawler in b.teams[winTeamIndex]:
            winTeam.append(brawler["brawler"]["name"])
        for brawler in b.teams[loseTeamIndex]:
            loseTeam.append(brawler["brawler"]["name"])
    
    #SORT AND RETURN TEAMS
    winTeam=sorted(winTeam)
    loseTeam=sorted(loseTeam)
    return winTeam, loseTeam

def EXTRACT_SOLO_RESULT(battle):
    """
    Desc:   RETURN SORTED WIN AND LOSE TEAM BASED ON BATTLE
    """
    winTeam=[]
    loseTeam=[]

    b = Battle(battle)
    if b.mode== "duoShowdown":
        if b.rank <=2:
            for brawler in b.get_team_of_player():
                winTeam.append(brawler["brawler"]["name"])
        else:
            for brawler in b.get_team_of_player():
                loseTeam.append(brawler["brawler"]["name"])
    elif b.mode == "soloShowdown":
        if b.rank <=4:
            winTeam.append(b.get_team_of_player()["brawler"]["name"])
        else:
            loseTeam.append(b.get_team_of_player()["brawler"]["name"])

    elif b.mode != "soloShowdown":
        #FIND INDEX WIN AND LOSE TEAM
        winTeamIndex=1
        loseTeamIndex=0
        for game_player in b.teams[0]:
            if (str(b.starTag) == str(game_player["tag"])):
                winTeamIndex=0
                loseTeamIndex=1

        #COLLECT BRAWLERS IN EACH TEAM
        
        for brawler in b.teams[winTeamIndex]:
            winTeam.append(brawler["brawler"]["name"])
        for brawler in b.teams[loseTeamIndex]:
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

def STORE_BEST_TEAM(dirName):
    dirName=".."+path_separator+"data"+path_separator+"battles"
    winTeams=[]
    loseTeams=[]
    for root, subdirectories, files in os.walk(dirName):
        for file in files:
            #READ BATTLES
            #with open("../data/battles/"+mode+"/"+map+"/"+startTime+"_"+mode+"_"+map+".json", 'r') as f:
            mode=os.path.join(root, file).split(path_separator)[-1].split("_")[1]
            map=os.path.join(root, file).split(path_separator)[-1].split("_")[2]
            startTime=os.path.join(root, file).split(path_separator)[-1].split("_")[0]
            with open(os.path.join(root, file), 'r') as f:
                battles_mode_map = json.load(f)

            winTeams.clear()
            loseTeams.clear()

            #GET WIN AND LOSE TEAMS
            for battle in battles_mode_map:
                winTeam, loseTeam = EXTRACT_TEAM_RESULT(battle)
                winTeam_set = set(winTeam)
                if len(winTeam) == len(winTeam_set):
                    if len(winTeam)>0:#to avoid adding void team due to duoshowdown
                        winTeams.append(winTeam)
                    if len(loseTeam)>0:
                        loseTeams.append(loseTeam)
            
            winTeamsUnique=[]
            winTeamsUnique=remove_team_duplicate(winTeams)
            loseTeamsUnique=[]
            loseTeamsUnique=remove_team_duplicate(loseTeams)

            winTable={}
            winList=[]
            total = 0

            for team in winTeamsUnique:
                pickNumber=winTeams.count(team)+loseTeams.count(team)
                total = total + pickNumber
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
                winList.append(win_dict)
                winTable["teams"]= winList
                winTable["battlesNumber"]=total
            filename = "../data/stats/teams/"+os.path.join(root, file).split(path_separator)[-1]
            with open(filename, 'w') as fp:
                json.dump(winTable, fp, indent=4)

def STORE_BEST_SOLO(dirName):
    dirName=".."+path_separator+"data"+path_separator+"battles"
    bestSolos={}
    
    for root, subdirectories, files in os.walk(dirName):
        for file in files:
            #READ BATTLES
            #with open("../data/battles/"+mode+"/"+map+"/"+startTime+"_"+mode+"_"+map+".json", 'r') as f:
            mode=os.path.join(root, file).split(path_separator)[-1].split("_")[1]
            map=os.path.join(root, file).split(path_separator)[-1].split("_")[2]
            startTime=os.path.join(root, file).split(path_separator)[-1].split("_")[0]
            with open(os.path.join(root, file), 'r') as f:
                battles_mode_map = json.load(f)

            bestSolos.clear()

            #GET WIN AND LOSE TEAMS
            for battle in battles_mode_map:
                winTeam, loseTeam = EXTRACT_SOLO_RESULT(battle)
                winTeam_set = set(winTeam)
                if len(winTeam) == len(winTeam_set):
                    if len(winTeam)>0:#to avoid adding void team due to duoshowdown
                        for player in winTeam:
                            if player in bestSolos:
                                bestSolos[player]["wins"]=bestSolos[player]["wins"]+1
                            else:
                                bestSolos[player]={}
                                bestSolos[player]["wins"]=1
                                bestSolos[player]["loses"]=0
                    if len(loseTeam)>0:
                        for player in loseTeam:
                            if player in bestSolos:
                                bestSolos[player]["loses"]=bestSolos[player]["loses"]+1
                            else:
                                bestSolos[player]={}
                                bestSolos[player]["wins"]=0
                                bestSolos[player]["loses"]=1
            
            winTable={}
            winList=[]
            total = 0

            for brawler in bestSolos:
                pickNumber=bestSolos[brawler]["wins"]+bestSolos[brawler]["loses"]
                total = total + pickNumber
                if(bestSolos[brawler]["loses"]==0):
                    winRate=1
                else:
                    winRate=bestSolos[brawler]["wins"]/pickNumber
                win_dict = {
                    "mode": mode,
                    "map": map,
                    "startTime": startTime, #start day
                    "soloStats": {
                        "winNumber": bestSolos[brawler]["wins"],
                        "winRate":winRate,
                        "pickRate": pickNumber/(len(battles_mode_map)),
                        "pickNumber":pickNumber,
                        "brawler": brawler
                        }
                }                    
                winList.append(win_dict)
                winTable["brawler"]= winList
                winTable["battlesNumber"]=total
            filename = "../data/stats/solo/"+os.path.join(root, file).split(path_separator)[-1]
            with open(filename, 'w') as fp:
                json.dump(winTable, fp, indent=4)
    

def STORE_BATTLES(battlelogsList):
    files2save={}
    go=False
    numberOfBattles=0
    battleNotInEvent=0
    total=0
    listNumOfBattles=[]
    newBattle=0
    alreadyStoredBattle=0
    notInterestingBattle=0
    friendlyBattles=0
    battleWithNoDuration=0
    curentEvent=READ_CURRENT_EVENTS("TODO")
    dataFolder = Path("../data/battles")
    dataFolder.mkdir(parents=True, exist_ok=True)
 
    for pays in battlelogsList:
        for players in battlelogsList[pays]:
            if "items" in battlelogsList[pays][players]:
                numberOfBattles=0
                for battles in battlelogsList[pays][players]["items"]:
                    if numberOfBattles <5:
                        numberOfBattles=numberOfBattles+1
                        total=total+1
                        #print(battles)
                        b = Battle(battles)
                        go = False

                        if b.mode=="gemGrab" or b.mode=="brawlBall" or b.mode=="heist" or b.mode=="bounty" or b.mode=="hotZone" or b.mode=="siege":
                            if not b.noDuration and not b.noResult and not b.noStarPlayer and not b.noType and not b.noTeams and b.typee!= "friendly":
                                go=True
                        elif b.mode=="soloShowdown" or b.mode=="duoShowdown":
                            if not b.noType and b.typee!= "friendly":
                                go=True

                        if go:
                            startTime=None
                            mode=b.mode
                            mapEvent=b.mapEvent
                            for event in curentEvent:
                                battleMap=event["event"]["map"]
                                battleMode=event["event"]["mode"]
                                if battleMap== mapEvent and battleMode== mode:
                                    startTime=event["startTime"]
                                    break
                            if startTime is not None:
                                modeFolder= dataFolder/mode
                                modeFolder.mkdir(parents=True, exist_ok=True)
                                mapFolder=modeFolder/mapEvent
                                mapFolder.mkdir(parents=True, exist_ok=True)
                                startTime=startTime.split(".")[0]

                                fileName=startTime+"_"+mode+"_"+mapEvent+".json"
                                mapFile=mapFolder/fileName
                                if mapFile.is_file() or mapFile in files2save:
                                    if mapFile not in files2save:
                                        data = json.load(open(mapFile))
                                        # convert data to list if not
                                        if type(data) is dict:
                                            data = [data]
                                        files2save[mapFile]=data
                                    alreadyExist=False
                                    for batailles in files2save[mapFile]:
                                        savedB=Battle(batailles)
                                        if savedB.is_equal(b):
                                            alreadyExist=True

                                    if not alreadyExist:
                                        # append new item to data lit
                                        files2save[mapFile].append(battles)
                                        newBattle=newBattle+1
                                        # write list to file
                                        '''
                                        with open(mapFile, 'w') as outfile:
                                            json.dump(data, outfile, indent=4)
                                            
                                        '''
                                    else:
                                        alreadyStoredBattle=alreadyStoredBattle+1
                                else:
                                    files2save[mapFile]=[battles]
                                    newBattle=newBattle+1
                                    '''
                                    with open(mapFile, 'w') as outfile:
                                        json.dump(battles, outfile, indent=4)
                                    '''  
                            else:
                                battleNotInEvent=battleNotInEvent+1
                        else:
                            if not b.noType and b.typee=="friendly":
                                friendlyBattles=friendlyBattles+1
                            elif b.noDuration:
                                battleWithNoDuration=battleWithNoDuration+1
                            else:
                                notInterestingBattle=notInterestingBattle+1

                   
            listNumOfBattles.append(numberOfBattles)
    print("--------------------------------------------------------")
    total= notInterestingBattle+alreadyStoredBattle+newBattle+battleNotInEvent+friendlyBattles+battleWithNoDuration
    print("New battles stored: "+ str(newBattle)+"/"+str(total))
    print("Battle not in curent event: "+ str(battleNotInEvent)+"/"+str(total))
    print("Already stored battles: "+ str(alreadyStoredBattle)+"/"+str(total))
    print("Not interesting battles: "+str(notInterestingBattle)+"/"+str(total))
    print("Friendly battles: ", str(friendlyBattles)+"/"+str(total))
    print("Battle with no duration: ",  str(battleWithNoDuration)+"/"+str(total))
    print("--------------------------------------------------------")
    print("total: ", total)
    print("min number of battle per battle log: ", min(listNumOfBattles))
    print("max number of battle per battle log: ", max(listNumOfBattles))
    print("mean number of battle per battle log: ", sum(listNumOfBattles)/len(listNumOfBattles))
    for files in files2save:
        with open(files, 'w') as outfile:
            json.dump(files2save[files], outfile, indent=4)


'''
    For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName):

    for root, subdirectories, files in os.walk(dirName):
        for file in files:
            print(os.path.join(root, file))