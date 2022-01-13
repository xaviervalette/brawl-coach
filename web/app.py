from flask import Flask, render_template, request, redirect, url_for
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../python')
from functions import *

app = Flask(__name__)
token=READ_API_TOKEN("../python/token.txt")


@app.route("/", methods=['GET', 'POST'])
def homepage():
	request_method=request.method
	if request.method == "POST":
		tag = request.form["tag"]
		print(request.form)
		return redirect(url_for('tag_results', tag=tag))
	return render_template('home.html')

@app.route("/explore/modes")
def modes():
	return render_template('modes.html')

@app.route("/tag_reader/<string:tag>")
def tag_results(tag):
	if(tag==""):
		return redirect(url_for('tag_not_found'))

	battlelogs = GET_PLAYER_STATS(token, tag)
	try:
		if battlelogs["reason"]=="notFound":
			return redirect(url_for('tag_not_found'))
	except:
		#return battlelogs
		looseNumber=0
		winNumber=0
		drawNumber=0
		starNumber=0
		result=[]
		for battle in battlelogs['items']:
			print(battle)
			try:
				if battle["battle"]["starPlayer"]["tag"]==tag:
					battle.update({"isStarPlayer":"yes"})
					starNumber=starNumber+1
				else:
					battle.update({"isStarPlayer":"no"})
			except:
					battle.update({"isStarPlayer":"N/A"})
			
			try:
				if battle["battle"]["result"]=="victory":
					winNumber=winNumber+1
					result.append("victory")
				elif battle["battle"]["result"]=="defeat":
					looseNumber=looseNumber+1
					result.append("defeat")
				else:
					drawNumber=drawNumber+1
					result.append("draw")

			except:
				try:
					if battle["battle"]["rank"]<5:
						winNumber=winNumber+1
						result.append("victory")
					elif battle["battle"]["rank"]>5:
						looseNumber=looseNumber+1
						result.append("defeat")
					else:
						drawNumber=drawNumber+1
						result.append("draw")
				except:
					result.append("N/A")


		return render_template('tag_results.html', battlelogs=battlelogs, len=len(battlelogs["items"]), tag=tag, starNumber=starNumber, winNumber=winNumber, looseNumber=looseNumber, drawNumber=drawNumber, result=result)

@app.route("/tag_reader/tag_not_found")
def tag_not_found():
	return "TO DO - NOT FOUND"

@app.route("/tag_reader/")
def tag_reader():
	return render_template('tag_reader.html')


@app.route("/modes/<string:mode>/maps")
def modes_maps(mode):
		return mode

@app.route("/solo_picker")
def solo_picker():
	battleNumber={}
	bestTeams={}
	current_events = READ_CURRENT_EVENTS("../events/current_events.json")
	for events in current_events:
		map=events["event"]["map"]
		mode=events["event"]["mode"]
		startTime=events["startTime"].split(".")[0]
		try:
			mode_map_details, battleNum =READ_EVENTS_STATS(mode,map, startTime, "solo")
			mode_map_details_sorted = sorted(mode_map_details, key=lambda d: d['soloStats']["pickRate"], reverse=True)
			bestTeams[mode]={map:mode_map_details_sorted}
			battleNumber[mode]={map:battleNum}
		except:
			battleNumber[mode]={map:"N/A"}
			bestTeams[mode]={map:"N/A"}
			
	return render_template('solo_picker.html', current_events=current_events, len=len(current_events), battleNumber=battleNumber, mode_map_details=bestTeams)		

@app.route("/team_picker")
def team_picker():
	battleNumber={}
	bestTeams={}
	current_events = READ_CURRENT_EVENTS("../events/current_events.json")
	for events in current_events:
		map=events["event"]["map"]
		mode=events["event"]["mode"]
		startTime=events["startTime"].split(".")[0]
		try:
			mode_map_details, battleNum =READ_EVENTS_STATS(mode,map, startTime, "teams")
			mode_map_details_sorted = sorted(mode_map_details, key=lambda d: d['teamStats']["pickRate"], reverse=True)
			bestTeams[mode]={map:mode_map_details_sorted}
			battleNumber[mode]={map:battleNum}
		except:
			battleNumber[mode]={map:"N/A"}
			bestTeams[mode]={map:"N/A"}
			
	return render_template('team_picker.html', current_events=current_events, len=len(current_events), battleNumber=battleNumber, mode_map_details=bestTeams)

@app.route("/teampicker/<string:mode>/<string:map>/<string:startTime>")
def mode_map(mode, map, startTime):
	try:	
		startTime=startTime.split(".")[0]
		mode_map_details_teams, battleNumTeam=READ_EVENTS_STATS(mode,map, startTime, "teams") #READ DATA FROM NATHAN
		mode_map_details_solo, battleNumSolo=READ_EVENTS_STATS(mode,map, startTime, "solo") #READ DATA FROM NATHAN
		mode_map_details_team_sorted = sorted(mode_map_details_teams, key=lambda d: d['teamStats']["pickRate"], reverse=True) 
		mode_map_details_solo_sorted = sorted(mode_map_details_solo, key=lambda d: d['teamStats']["pickRate"], reverse=True) 
		if len(mode_map_details_team_sorted)>50:
			team_number=50
		else:
			team_number=len(mode_map_details_team_sorted)
		
		if len(mode_map_details_solo_sorted)>50:
			solo_number=50
		else:
			solo_number=len(mode_map_details_solo_sorted)
		return render_template('mode_map_details.html', mode_map_details_team=mode_map_details_team_sorted, mode_map_details_solo=mode_map_details_solo_sorted, team_number=team_number, solo_number=solo_number, mode=mode, map=map)
	except:
		return "TO DO"

@app.route("/solopicker/<string:mode>/<string:map>/<string:startTime>")
def mode_map_solo(mode, map, startTime):
	#try:	
	startTime=startTime.split(".")[0]
	mode_map_details, battleNum=READ_EVENTS_STATS(mode,map, startTime, "solo") #READ DATA FROM NATHAN
	mode_map_details_sorted = sorted(mode_map_details, key=lambda d: d['soloStats']["pickRate"], reverse=True) 
	if len(mode_map_details)>50:
		team_number=50
	else:
		team_number=len(mode_map_details)
	return render_template('mode_map_details_solo.html', mode_map_details=mode_map_details_sorted, len=team_number, mode=mode, map=map)
	#except:
		#return "TO DO"

@app.route("/processTime.log")
def processTime():
	try:
		with open(logPath+path_separator+"timeLog.txt") as fp:
			timeLog = json.load(fp)
	except:
		timeLog=[]
	return {"items": timeLog}


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)
