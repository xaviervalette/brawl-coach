from functions import *

getListOfFiles("..\\data\\battles")
#Global variables
player_limit=200

countries_list=["FR","US", "JP", "DE"]
token=READ_API_TOKEN("token.txt")


print("\n***GET_RANKINGS***\n")
ranks=GET_RANKINGS(token,countries_list, player_limit) #ranks["FR"]["items"][0] = Best french player
print("\n***GET_BATTLELOGS***\n")
battlelogs=GET_BATTLELOGS(token, ranks) #battlelogs["FR"]["#2QC8VJ2"]["items"][0] = First battle of french player #2QC8VJ2
STORE_BATTLES(battlelogs)