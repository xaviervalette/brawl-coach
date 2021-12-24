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
	battlelogs = GET_PLAYER_STATS(token, tag)
	try:
		if battlelogs["reason"]=="notFound":
			return redirect(url_for('tag_not_found'))
	except:
		#return battlelogs
		looseNumber=0
		winNumber=0
		starNumber=0
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
			if battle["battle"]["result"]=="victory":
				winNumber=winNumber+1
			else:
				looseNumber=looseNumber+1

		return render_template('tag_results.html', battlelogs=battlelogs, len=len(battlelogs["items"]), tag=tag, starNumber=starNumber, winNumber=winNumber, looseNumber=looseNumber)

@app.route("/tag_reader/tag_not_found")
def tag_not_found():
	return "TO DO - NOT FOUND"

@app.route("/modes/<string:mode>/maps")
def modes_maps(mode):
		return mode

@app.route("/team_picker")
def team_picker():
	current_events = READ_CURRENT_EVENTS("../events/current_events.json")
	return render_template('team_picker.html', current_events=current_events, len=len(current_events))

@app.route("/teampicker/<string:mode>/<string:map>")
def mode_map(mode, map):
	try:	
		mode_map_details=READ_EVENTS_STATS(mode,map) #READ DATA FROM NATHAN
		mode_map_details_sorted = sorted(mode_map_details, key=lambda d: d['teamStats']["pickRate"], reverse=True) 
		if len(mode_map_details)>50:
			team_number=50
		else:
			team_number=len(mode_map_details)
		return render_template('mode_map_details.html', mode_map_details=mode_map_details_sorted, len=team_number, mode=mode, map=map)
	except:
		return "TO DO"
	

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)
