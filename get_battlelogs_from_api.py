import json
import requests

def get_rank_from_api():
#GET the rank output

        url = "https://api.brawlstars.com/v1/rankings/FR/players"
        headers = {
          'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjBiOTgxN2M5LWIyZmUtNGZlZC1iZjhkLTMyN2VlMTgzNDk3MCIsImlhdCI6MTYzMDYwMDYwMCwic3ViIjoiZGV2ZWxvcGVyLzk2NWU0ZGI3LTU3YTMtM2FhYy1hYmNhLWE2NzEzODI5NWJiMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTUuMTg4LjQ3LjE4NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.-onaSw0J63JhTCBmAonb6ZokEhFDJHs12GD5h8giJ7Y023oCzv0NJq0DqDxefNlfdo91c_iWAth1OF6U787fKA'
        }
        payload={}
        response = requests.request("GET", url, headers=headers, data=payload)
        ranks=response.json()
        return ranks

def get_tag_from_rank(rank):
#Extract TAG value (e.g. #RQRLVV9C) from the GET rank call output

        tags=[]
        for i in rank['items']:
                tags.append(i["tag"])
        return tags

def get_battlelog_from_tag(tags):
#GET battlelogs for each TAG extracted from the rank

        battlelogs=[]
        i=0
        for tag in tags:
                headers = {
                'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjBiOTgxN2M5LWIyZmUtNGZlZC1iZjhkLTMyN2VlMTgzNDk3MCIsImlhdCI6MTYzMDYwMDYwMCwic3ViIjoiZGV2ZWxvcGVyLzk2NWU0ZGI3LTU3YTMtM2FhYy1hYmNhLWE2NzEzODI5NWJiMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTUuMTg4LjQ3LjE4NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.-onaSw0J63JhTCBmAonb6ZokEhFDJHs12GD5h8giJ7Y023oCzv0NJq0DqDxefNlfdo91c_iWAth1OF6U787fKA'
                }
                url_tag=tag.replace("#","%23")
                payload={}
                response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=payload)
                print(response)
                battlelogs.append(response.json())

ranks=get_rank_from_api()
tags=get_tag_from_rank(ranks)
battlelogs=get_battlelog_from_tag(tags)
