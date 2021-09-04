import json

with open("data.json") as f:
    data = json.load(f)

for item in data:
    print(item['items'])
    for battle in item['items']:
        print (battle['battle'])
        exit()
