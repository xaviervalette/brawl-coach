from functions import *
import time

start = time.time()

#Global variables
player_limit=200

countries_list=["FR", "JP", "DE", "BR", "ES", "US", "RU", "CA", "IT", "GB"]
token=READ_API_TOKEN("token.txt")

GET_CURRENT_EVENTS(token)

print("\n***GET_RANKINGS***\n")
ranks=GET_RANKINGS(token,countries_list, player_limit) #ranks["FR"]["items"][0] = Best french player
print("\n***GET_BATTLELOGS***\n")
battlelogs=GET_BATTLELOGS(token, ranks) #battlelogs["FR"]["#2QC8VJ2"]["items"][0] = First battle of french player #2QC8VJ2
end = time.time()
callTime=end - start
start2 = time.time()
STORE_BATTLES(battlelogs)
end2 = time.time()
processTime=end2 - start2

print("Time for all API calls: ", callTime, "s")
print("Time for store process: ", processTime, "s")

STORE_BEST_TEAM("TODO")