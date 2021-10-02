import json
import requests
import datetime

home="/home/ec2-user/brawl-tier/"
date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
country_code_list=sorted(["global"])

def read_api_token(filename):
	"""
	Desc:	Read the API token from a file
	Input:	filename
	Output: API token
	"""
	infile = open(home+filename, 'r')
	data = infile.read()
	infile.close()
	return data.strip()

def get_rank_from_api(token,country_code):
	"""
	Desc:   GET tags of leaderboard
	Input:  API token
	Output: A 200 player json file
	"""
	ranks={}
	url = "https://api.brawlstars.com/v1/rankings/"+country_code+"/powerplay/seasons/104"
	headers = {
	'Authorization':'Bearer '+token
	}
	payload={}
	response = requests.request("GET", url, headers=headers, data=payload)
	data=response.json()
	return data

def get_tag_from_rank(rank):
	"""
	Desc:   GET tags of json file
	Input: 	Leaderboard API response
	Output: A 200 tag list
	"""
	tags=[]
	for i in rank['items']:
        	tags.append(i["tag"])
	filename = home+"/powerPlay/tags/tags_"+date+"_"+country_code+".json"
  	with open(filename, 'w') as fp:
    		for item in tags:
			fp.write("%s\n" % item)
 	return tags

def get_history_from_tag(tags,token,country_code):
	"""
	Desc:   GET battlelogs from tag list
	Input:  A list of tags
	Output: A battlelogs json file of the tags in input
	"""
	battlelogs=[]
	filename = home+"/powerPlay/battlelogs/battlelogs_"+date+"_"+country_code+".json"
	for tag in tags:
		headers = {
	  	'Authorization': 'Bearer '+token
		}
		url_tag=tag.replace("#","%23")
		payload={}
		response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=payload)
		battlelogs.append(response.json())
	with open(filename, 'w') as fp:
    		json.dump(battlelogs, fp)

token=read_api_token("token.txt")
for country_code in country_code_list:
	print(country_code+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
	ranks=get_rank_from_api(token,country_code)
	tags=get_tag_from_rank(ranks)
	history=get_history_from_tag(tags,token, country_code)
