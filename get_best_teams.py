import json
from collections import defaultdict
import os
import glob
import datetime

base_dir = '/home/ec2-user/brawl-tier/battlelogs/battlelogs_20210926/*'
home="/home/ec2-user/brawl-tier/"
with open("events/events_20210926-100630.json") as f:
    events = json.load(f)

target_event=events[2]
print(target_event)
#battelogs[player_number{0-200}]["items"][game_number{0-25}]["event"]["id"]

winning_team=[]
loosing_team=[]


battlelogs_list=[]
filepaths = glob.glob(base_dir)
for fp in filepaths:
        with open(fp, 'r') as f:
                # Read the first line
                battlelogs = json.load(f)
                # Append the first line into the list
                battlelogs_list.append(battlelogs)
game_number_targeted_event=0
for battlelogs in battlelogs_list:
        for player in battlelogs:
                for game in player["items"]:
                        #print(game["event"]["id"])
			if(game["event"]["id"]==target_event["event"]["id"]):
				game_number_targeted_event=game_number_targeted_event+1
				star_player=game["battle"]["starPlayer"]
				if star_player in game["battle"]["teams"][0]:
					winning_team_index=False
				else:
					winning_team_index=True
				winners=[]
				loosers=[]
				for brawler in game["battle"]["teams"][winning_team_index]:
					winners.append(brawler["brawler"]["name"])
				for brawler in game["battle"]["teams"][not(winning_team_index)]:
					loosers.append(brawler["brawler"]["name"])
				winners=sorted(winners)
				winning_team.append(winners)
				loosers=sorted(loosers)
				loosing_team.append(loosers)

print "Number of game corresponding to the targeted event:",game_number_targeted_event

def remove_team_duplicate(team):
	team_no_dupplicate=[]
	for elem in team:
		if elem not in team_no_dupplicate:
			team_no_dupplicate.append(elem)
	return team_no_dupplicate

winning_team_no_dupplicate=remove_team_duplicate(winning_team)
loosing_team_no_dupplicate=remove_team_duplicate(loosing_team)

win_table=[]

for team in winning_team_no_dupplicate:
	#win_table.append([winning_team.count(team),team])
	if(loosing_team.count(team)==0):
		win_rate=1
	else:
		win_rate=float(winning_team.count(team))/float((winning_team.count(team)+loosing_team.count(team)))
	win_dict = {
		"teamStats": {
			"winNumber": winning_team.count(team),
			"winRate":round(win_rate,3),
			"pickRate": round((winning_team.count(team)+loosing_team.count(team))/float(game_number_targeted_event),3),
			"pickNumber":winning_team.count(team)+loosing_team.count(team),
			"brawlers": team
			}
	}
	win_table.append(win_dict)
	#print("Team:",team,"Count",winning_team.count(team))

print(win_table[0])

win_table = sorted(win_table, key=lambda win_table: win_table['teamStats']["pickNumber"], reverse=True)

event_dict={"gameMode": target_event}

win_table.append(event_dict)

filename = home+"/teamStats/teamStats_"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".json"
with open(filename, 'w') as fp:
	json.dump(win_table, fp)
