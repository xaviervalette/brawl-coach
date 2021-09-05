import json

with open("data.json") as f:
    datas = json.load(f)

for data in datas:
    print(data['items'])
    for item in data['items']:
        print (item['event'])
        exit()
