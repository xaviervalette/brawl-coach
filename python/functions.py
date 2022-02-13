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

"""
SETTING GLOBAL VARIABLES
"""
if(platform.system()=="Windows"):
    path_separator="\\"
else:
    path_separator="/"

dataPath=".."+path_separator+".."+path_separator+"data"
logPath=".."+path_separator+".."+path_separator+"log"

"""
READ AND RETURN BRAWL STARS API JSON WEB TOKEN
"""
def readApiToken(filepath):
    infile = open(filepath, 'r')
    data = infile.read()
    infile.close()
    return data.strip()

"""
MAKE REST API GET CALL TO RETRIEVE BRAWL STARS SPECIFIC PLAYER STATS USING PLAYER TAG
"""
def getPlayerStats(token, tag):
    headers = {'Authorization':'Bearer '+token}
    data={}
    url_tag=tag.replace("#","%23")
    response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=data)
    battlelogs = response.json()
    return battlelogs

"""
MAKE REST API GET CALL TO RETRIEVE BRAWL STARS CURRENT EVENTS
"""
def getCurrentEvents(token):

    f = []
    for (dirpath, dirnames, filenames) in os.walk(dataPath+"/events/"):
        f.extend(filenames)
        break
    old_current_events=readCurrentEvents("todo")
    headers = {'Authorization':'Bearer '+token}
    data={}
    response = requests.request("GET", "https://api.brawlstars.com/v1/events/rotation", headers=headers, data=data)
    current_events = response.json()
    i=0
    for event in current_events:
        print(event)
        if old_current_events[i]["event"]["id"]!=event["event"]["id"]:
            try:
                os.remove(dataPath+"/battles/"+str(i)+".json")
                os.remove(dataPath+"/stats/"+str(i)+".json")
            except:
                print("No battles recorded during the whold event")
        event["currentEventNumber"]=i
        i=i+1
    with open(dataPath+'/events/current_events.json', 'w') as f:
        json.dump(current_events, f)
    return

"""
READ AND RETURN BRAWL STARS CURRENT EVENTS
"""
def readCurrentEvents(filepath):
    with open(dataPath+'/events/current_events.json') as f:
        current_events=json.load(f)
    return current_events

"""
READ AND RETURN BRAWL STARS EVENTS STATS
"""
def readEventsStats(event, soloOrTeams):
    if soloOrTeams=="teams":
        with open(dataPath+'/stats/'+str(event["currentEventNumber"])+'.json') as f:
            events_stats=json.load(f)
        return events_stats["teams"], events_stats["battlesNumber"]
    else:
        with open(dataPath+'/stats/'+str(event["currentEventNumber"])+'.json') as f:
            events_stats=json.load(f)
        return events_stats["solo"], events_stats["battlesNumber"]

"""
MAKE REST API GET CALL TO RETRIEVE BRAWL STARS RANKINGS BASED ON COUNTRY LIST
"""
def getRankings(token,countries_list,player_limit):
    ranks_list={}
    headers = {'Authorization':'Bearer '+token}
    data={}
    for country in countries_list:
        url = "https://api.brawlstars.com/v1/rankings/"+country+"/players?limit="+str(player_limit)
        response = requests.request("GET", url, headers=headers, data=data)
        ranks_list[country]=response.json()
        print("Country:" + country + ", Response code: " + str(response.status_code))
    return ranks_list

"""
MAKE REST API GET CALL TO RETRIEVE BRAWL STARS RANKINGS BASED ON COUNTRY LIST
"""
def getBattlelogs(token, ranks_list):
    battlelogs_list={}
    battlelogs={}
    threads= []
    with ThreadPoolExecutor(max_workers=40) as executor:

        for country in ranks_list:
            battlelogs.clear()
            threads.append(executor.submit(getBattlelogsApiCalls, country, ranks_list, battlelogs, token))
            
        for task in as_completed(threads):
            done=True 
        battlelogs_list[country]=battlelogs
    return battlelogs_list

"""
MAKE REST API GET CALL TO RETRIEVE BRAWL STARS RANKINGS BASED ON COUNTRY LIST - THREAD
"""
def getBattlelogsApiCalls(country, ranks_list, battlelogs, token):
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
        #print("Country:" + country + ", Tag: "+ tag + ", Response code: " + str(response.status_code))
    return battlelogs

"""
RETURN SORTED WIN AND LOSE TEAM BASED ON BATTLE
"""
def extractTeamBattles(battle):
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

def extractSoloBattles(battle):
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

def computeBestBrawlers(mode,map, startTime):
    mode="gemGrab"
    map="Four Squared"
    startTime="20212212"

    #READ BATTLES
    with open(dataPath+path_separator+'battles'+path_separator+mode+path_separator+map+path_separator+startTime+"_"+mode+"_"+map+".json", 'r') as f:
        battles_mode_map = json.load(f)
    for battle in battles_mode_map:
        winTeam, loseTeam = extractTeamBattles(battle)

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

def storeBestTeam():
    dataFolder = Path(dataPath+path_separator+"battles")
    dataFolder.mkdir(parents=True, exist_ok=True)
    currentEvent=readCurrentEvents("TODO")
    i=0
    for event in currentEvent:
        map=event["event"]["map"]
        mode=event["event"]["mode"]
        startTime=event["startTime"]
        winTeams=[]
        loseTeams=[]
        try:
            with open(dataPath+path_separator+"battles"+path_separator+str(event["currentEventNumber"])+".json", 'r') as f:
                battles_mode_map = json.load(f)
        except:
            print("NO DATA")
            continue

        winTeams.clear()
        loseTeams.clear()
        bestSolos={}

        #GET WIN AND LOSE TEAMS
        for battle in battles_mode_map:
            winTeam, loseTeam = extractTeamBattles(battle)
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

        for team in winTeamsUnique:
            pickNumber=winTeams.count(team)+loseTeams.count(team)
            if(loseTeamsUnique.count(team)==0):
                winRate=1
            else:
                winRate=winTeams.count(team)/pickNumber
            win_dict = {
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
        
                #GET WIN AND LOSE TEAMS
        for battle in battles_mode_map:
            winSolo, loseSolo = extractSoloBattles(battle)
            winSolo_set = set(winSolo)
            if len(winSolo) == len(winSolo_set):
                if len(winSolo)>0:#to avoid adding void team due to duoshowdown
                    for player in winSolo:
                        if player in bestSolos:
                            bestSolos[player]["wins"]=bestSolos[player]["wins"]+1
                        else:
                            bestSolos[player]={}
                            bestSolos[player]["wins"]=1
                            bestSolos[player]["loses"]=0
                if len(loseSolo)>0:
                    for player in loseSolo:
                        if player in bestSolos:
                            bestSolos[player]["loses"]=bestSolos[player]["loses"]+1
                        else:
                            bestSolos[player]={}
                            bestSolos[player]["wins"]=0
                            bestSolos[player]["loses"]=1
        
        winListSolo=[]

        for brawler in bestSolos:
            pickNumber=bestSolos[brawler]["wins"]+bestSolos[brawler]["loses"]
            if(bestSolos[brawler]["loses"]==0):
                winRate=1
            else:
                winRate=bestSolos[brawler]["wins"]/pickNumber
            win_dict = {
                "soloStats": {
                    "winNumber": bestSolos[brawler]["wins"],
                    "winRate":winRate,
                    "pickRate": (pickNumber/(len(battles_mode_map)))/2,
                    "pickNumber":pickNumber,
                    "brawler": brawler
                    }
            }                    
            winListSolo.append(win_dict)
            winTable["solo"]= winListSolo
            winTable["battlesNumber"]=len(battles_mode_map)
            winTable["mode"]=mode
            winTable["map"]=map
            winTable["startTime"]=startTime
        
        filename = dataPath+"/stats/"+str(event["currentEventNumber"])+".json"
        with open(filename, 'w') as fp:
            json.dump(winTable, fp, indent=4)
    

def getListOfFiles(dirName):
    for root, subdirectories, files in os.walk(dirName):
        for file in files:
            print(os.path.join(root, file))

def storeBattles(battlelogsList, limitNumberOfBattles, expectedModes):
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
    curentEvent=readCurrentEvents("TODO")
    dataFolder = Path(dataPath+"/battles")
    dataFolder.mkdir(parents=True, exist_ok=True)
 
    for pays in battlelogsList:
        for players in battlelogsList[pays]:
            if "items" in battlelogsList[pays][players]:
                numberOfBattles=0
                for battles in battlelogsList[pays][players]["items"]:
                    if numberOfBattles <limitNumberOfBattles:
                        numberOfBattles=numberOfBattles+1
                        total=total+1
                        b = Battle(battles)
                        go = False

                        if b.mode in expectedModes:
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
                                startTime=startTime.split(".")[0]
                                fileName=str(event["currentEventNumber"])+".json"
                                mapFile=dataFolder/fileName
                                if mapFile.is_file() or mapFile in files2save:
                                    if mapFile not in files2save:
                                        data = json.load(open(mapFile))
                                        # convert data to list if not
                                        if type(data) is dict:
                                            data = [data]
                                        files2save[mapFile]=data
                                    alreadyExist=False

                                    if not alreadyExist:
                                        # append new item to data lit
                                        files2save[mapFile].append(battles)
                                        newBattle=newBattle+1

                                    else:
                                        alreadyStoredBattle=alreadyStoredBattle+1
                                else:
                                    files2save[mapFile]=[battles]
                                    newBattle=newBattle+1

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
    i=0
    for files in files2save:
        with open(files, 'w') as outfile:
            files2saveNoDupp=remove_dupe_dicts(files2save[files])
            json.dump(files2saveNoDupp, outfile, indent=4)
        i=i+1
    return newBattle, alreadyStoredBattle, total

'''
    For the given path, get the List of all files in the directory tree 
'''
def remove_dupe_dicts(l): 
    list_of_strings = [json.dumps(d, sort_keys = True) for d in l] 
    A=len(list_of_strings)
    list_of_strings = set(list_of_strings) 
    B=len(list_of_strings)
    return [json.loads(s) for s in list_of_strings]