from functions import *
import time
from datetime import datetime


#Global variables
player_limit=50
limitNumberOfBattles=5
logFileName="timeLog.txt"

countries_list=["FR", "US", "IT", "CA", "DE", "GR", "CN", "FI", "ES", "BR", "IN"]
token=READ_API_TOKEN("token.txt")

start2 = time.time()
GET_CURRENT_EVENTS(token)

print("\n***GET_RANKINGS***\n")
ranks=GET_RANKINGS(token,countries_list, player_limit) #ranks["FR"]["items"][0] = Best french player

print("\n***GET_BATTLELOGS***\n")
battlelogs=GET_BATTLELOGS(token, ranks) #battlelogs["FR"]["#2QC8VJ2"]["items"][0] = First battle of french player #2QC8VJ2
end2 = time.time()
callTime=end2 - start2

print("\n***STORE BATTLES***\n")
start3 = time.time()
newBattle=STORE_BATTLES(battlelogs, limitNumberOfBattles)
end3 = time.time()
storeBattleTime=end3 - start3

print("\n***COMPUTE BEST BRAWLER***\n")
start4 = time.time()
STORE_BEST_TEAM("TODO")
STORE_BEST_SOLO("TODO")
end4 = time.time()
computeBestBrawler=end4 - start4
now = datetime.now()
dateTime = now.strftime("%Y-%m-%d %H:%M:%S")
processHistory={"datetime":dateTime, "callTime":callTime, "storeBattleTime":storeBattleTime, "computeBestBrawler":computeBestBrawler, "countryNumber": len(countries_list), "playerNumber":player_limit, "newBattle":newBattle}

#WRITE LOGS
try:
    with open(logFileName) as fp:
        timeLog = json.load(fp)
except:
    timeLog=[]

timeLog.append(processHistory)
with open(logFileName, 'w') as json_file:
    json.dump(timeLog, json_file, 
                        indent=4)