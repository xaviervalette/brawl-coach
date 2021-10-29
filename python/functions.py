import json
import requests

def READ_API_TOKEN(filepath):
    """
    Desc:	Read the API token from a file
    Input:	String: filename
    Output: String: API token
    """
    infile = open(filepath, 'r')
    data = infile.read()
    infile.close()
    return data.strip()

def GET_RANKINGS(token,countries_list,player_limit):
    """
    Desc:   GET tags of leaderboard
    Input:  API token
    Output: A 200 player json file
    """
    ranks_list={}
    headers = {'Authorization':'Bearer '+token}
    data={}
    for country in countries_list:
        url = "https://api.brawlstars.com/v1/rankings/"+country+"/players?limit="+str(player_limit)
        response = requests.request("GET", url, headers=headers, data=data)
        ranks_list[country]=response.json()
        print("Country:" + country + ", Response code: " + str(response.status_code))
    return ranks_list

def GET_BATTLELOGS(token, ranks_list):
    """
    Desc:   GET battlelogs from tag list
    Input:  A list of tags
    Output: A battlelogs json file of the tags in input
    """
    battlelogs_list={}
    battlelogs={}
    headers = {'Authorization': 'Bearer '+token}
    data = {}
    for country in ranks_list:
        for player in ranks_list[country]['items']:
            tag=player["tag"]
            url_tag=tag.replace("#","%23")
            response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=data)
            battlelogs[tag]= response.json()
            print("Country:" + country + ", Tag: "+ tag + ", Response code: " + str(response.status_code))
        battlelogs_list[country]=battlelogs
    return battlelogs_list