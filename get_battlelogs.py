import json
import requests
import datetime

home="/home/ec2-user/brawl-tier/"

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

def get_rank_from_api(token):
	"""
	Desc:   GET tags of leaderboard
	Input:  API token
	Output: A 200 player json file
	"""
	url = "https://api.brawlstars.com/v1/rankings/FR/players"
	headers = {
	'Authorization':'Bearer '+token
	}
	payload={}
	response = requests.request("GET", url, headers=headers, data=payload)
	ranks=response.json()
	return ranks

def get_tag_from_rank(rank):
	"""
	Desc:   GET tags of json file
	Input: 	Leaderboard API response
	Output: A 200 tag list
	"""
	tags=[]
	for i in rank['items']:
        	tags.append(i["tag"])
	return tags

def get_history_from_tag(tags,token):
	"""
	Desc:   GET battlelogs from tag list
	Input:  A list of tags
	Output: A battlelogs json file of the tags in input
	"""
	battlelogs=[]
	filename = home+"/battlelogs/battlelogs_"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".json"
	#tags_first=[tags[0], tags[1]]
	for tag in tags:
		headers = {
	  	'Authorization': 'Bearer '+token
		}
		url_tag=tag.replace("#","%23")
		payload={}
		response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=payload)
		print(response)
		battlelogs.append(response.json())
		with open(filename, 'w') as fp:
    			json.dump(battlelogs, fp)

token=read_api_token("token.txt")
ranks=get_rank_from_api(token)
tags=get_tag_from_rank(ranks)
history=get_history_from_tag(tags, token)
