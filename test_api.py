import json
import requests

url = "https://api.brawlstars.com/v1/rankings/FR/players"

payload={}

def get_rank_from_api():
	headers = {
	  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjBiOTgxN2M5LWIyZmUtNGZlZC1iZjhkLTMyN2VlMTgzNDk3MCIsImlhdCI6MTYzMDYwMDYwMCwic3ViIjoiZGV2ZWxvcGVyLzk2NWU0ZGI3LTU3YTMtM2FhYy1hYmNhLWE2NzEzODI5NWJiMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTUuMTg4LjQ3LjE4NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.-onaSw0J63JhTCBmAonb6ZokEhFDJHs12GD5h8giJ7Y023oCzv0NJq0DqDxefNlfdo91c_iWAth1OF6U787fKA'
	}

	response = requests.request("GET", url, headers=headers, data=payload)
	ranks=response.json()
	return ranks

def get_tag_from_rank(rank):
	tags=[]
	for i in rank['items']:
        	tags.append(i["tag"])
	return tags

def get_history_from_tag(tags):
	print("to do")

ranks=get_rank_from_api()
tags=get_tag_from_rank(ranks)
print(tags)
