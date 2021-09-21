import json
import requests
import datetime

home="/home/ec2-user/brawl-tier/"
country_code_list=["AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG", "AR",
"AM", "AW", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE",
"BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW", "BV", "BR", "IO",
"BN", "BG", "BF", "BI", "CV", "KH", "CM", "CA", "KY", "CF", "TD",
"CL", "CN", "CX", "CC", "CO", "KM", "CG", "CD", "CK", "CR", "CI",
"HR", "CU", "CW", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG",
"SV", "GQ", "ER", "EE", "ET", "FK", "FO", "FJ", "FI", "FR", "GF",
"PF", "TF", "GA", "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD",
"GP", "GU", "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN",
"HK", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT",
"JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG",
"LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MO", "MK",
"MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ", "MR", "MU", "YT",
"MX", "FM", "MD", "MC", "MN", "ME", "MS", "MA", "MZ", "MM", "NA",
"NR", "NP", "NL", "NC", "NZ", "NI", "NE", "NG", "NU", "NF", "MP",
"NO", "OM", "PK", "PW", "PS", "PA", "PG", "PY", "PE", "PH", "PN",
"PL", "PT", "PR", "QA", "RE", "RO", "RU", "RW", "BL", "SH", "KN",
"LC", "MF", "PM", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC",
"SL", "SG", "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES",
"LK", "SD", "SR", "SJ", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ",
"TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC", "TV",
"UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU", "VE", "VN",
"VG", "VI", "WF", "EH", "YE", "ZM", "ZW"]

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
	url = "https://api.brawlstars.com/v1/rankings/"+country_code+"/players"
	headers = {
	'Authorization':'Bearer '+token
	}
	payload={}
	response = requests.request("GET", url, headers=headers, data=payload)
	ranks=response.json()
	#print(response)
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

def get_history_from_tag(tags,token,country_code):
	"""
	Desc:   GET battlelogs from tag list
	Input:  A list of tags
	Output: A battlelogs json file of the tags in input
	"""
	battlelogs=[]
	filename = home+"/battlelogs/battlelogs_"+country_code+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".json"
	for tag in tags:
		headers = {
	  	'Authorization': 'Bearer '+token
		}
		url_tag=tag.replace("#","%23")
		payload={}
		response = requests.request("GET", "https://api.brawlstars.com/v1/players/"+url_tag+"/battlelog", headers=headers, data=payload)
		#print(response)
		battlelogs.append(response.json())
		with open(filename, 'w') as fp:
    			json.dump(battlelogs, fp)

token=read_api_token("token.txt")

for country_code in country_code_list:
	print(country_code)
	ranks=get_rank_from_api(token,country_code)
	tags=get_tag_from_rank(ranks)
	history=get_history_from_tag(tags,token, country_code)
