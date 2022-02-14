from functions import *
import time
from datetime import datetime


"""
GLOBAL VARIABLES
"""
player_limit=150
limitNumberOfBattles=2
logFileName=logPath+path_separator+"timeLog.txt"
countries_list=["FR", "US", "IT", "CA", "DE", "GR", "CN", "FI", "ES", "BR", "IN"]
expectedModes=["gemGrab", "brawlBall", "heist", "bounty", "hotZone", "siege", "knockout"]

"""
MAIN
"""
token=readApiToken("token.txt")

start2 = time.time()
getCurrentEvents(token)
delOldEvents("battles")
delOldEvents("stats")

print("\n***getRankings***\n")
ranks=getRankings(token,countries_list, player_limit) #ranks["FR"]["items"][0] = Best french player

print("\n***getBattlelogs***\n")
battlelogs=getBattlelogs(token, ranks) #battlelogs["FR"]["#2QC8VJ2"]["items"][0] = First battle of french player #2QC8VJ2
end2 = time.time()
callTime=end2 - start2

print("\n***STORE BATTLES***\n")
start3 = time.time()
newBattle, interestingBattle, totalBattle=storeBattles(battlelogs, limitNumberOfBattles, expectedModes)
end3 = time.time()
storeBattleTime=end3 - start3

print("\n***COMPUTE BEST BRAWLER***\n")
start4 = time.time()
storeBestTeam()
end4 = time.time()
computeBestBrawler=end4 - start4

now = datetime.now()
dateTime = now.strftime("%Y-%m-%d %H:%M:%S")
processHistory={"datetime":dateTime, "callTime":callTime, "storeBattleTime":storeBattleTime, "computeBestBrawler":computeBestBrawler, "countryNumber": len(countries_list), "playerNumber":player_limit, "newBattle":newBattle, "dupBattle": interestingBattle, "interestingBattle": interestingBattle, "totalBattle":totalBattle, "countryList":countries_list}
print (processHistory)
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