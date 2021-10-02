import json
from collections import defaultdict
import os
import glob
import datetime

filepath = '/home/ec2-user/brawl-tier/powerPlay/battlelogs/battlelogs_20210926-151835_global.json'
home="/home/ec2-user/brawl-tier/"

#battelogs[player_number{0-200}]["items"][game_number{0-25}]["event"]["id"]

winning_team=[]
loosing_team=[]


battlelogs_list=[]
with open(filepath, 'r') as f:
	battlelogs = json.load(f)
battlelogs.pop(148)
soloMatch=0
teamMatch=0
i=0
for player in battlelogs:
	print(i)
	player_items=player["items"]
	for game in player_items:
		if(game["event"]["id"]==15000306):
			if(game["battle"]["type"]=="teamRanked"):
				teamMatch=teamMatch+1
			elif(game["battle"]["type"]=="soloRanked"):
				soloMatch=soloMatch+1
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
	i=i+1
print "Number of game corresponding to the solo targeted event:",soloMatch
print "Number of game corresponding to the team targeted event:",teamMatch

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
	total=soloMatch+teamMatch
	if(loosing_team.count(team)==0):
		win_rate=1
	else:
		win_rate=float(winning_team.count(team))/float((winning_team.count(team)+loosing_team.count(team)))
	win_dict = {
		"teamStats": {
			"winNumber": winning_team.count(team),
			"winRate":round(win_rate,3),
			"pickRate": round((winning_team.count(team)+loosing_team.count(team))/float(total),3),
			"pickNumber":winning_team.count(team)+loosing_team.count(team),
			"brawlers": team
			}
	}
	win_table.append(win_dict)

win_table = sorted(win_table, key=lambda win_table: win_table['teamStats']["pickNumber"], reverse=True)

event_dict={"gameMode": "TBD"}
team_dict={"overall": {"numberDiffTeams": len(winning_team_no_dupplicate)}}

win_table.append(team_dict)

filename = home+"/powerPlay/teamStats/teamStats_global_20210926-151835.json"
with open(filename, 'w') as fp:
	json.dump(win_table, fp)
