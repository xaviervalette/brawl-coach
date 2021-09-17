# <img src="https://user-images.githubusercontent.com/28600326/133853719-9c5c6942-89c8-42ef-bbb2-083f644cc824.png" width="20" height="20">  Brawl Stars - Brawler tiers from leaderboard analysis

- Brawl Stars REST API
- Retrieve player's information
- Process player's information

## Brawl Stars REST API (api.brawlstars.com)
Brawl Stars REST API is using __JSON Web Token__ for the authentication of the HTTPS requests.
### JSON Web Token (JWT)
> JSON Web Tokens are an open, industry standard RFC 7519 method for representing claims securely between two parties - https://jwt.io/

The structure of a JWT is the following: ```header.payload.signature```. Below is an example of a JWT provided by the Brawl Star API website:
#### Encoded
```jwt
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjBiOTgxN2M5LWIyZmUtNGZlZC1iZjhkLTMyN2VlMTgzNDk3MCIsImlhdCI6MTYzMDYwMDYwMCwic3ViIjoiZGV2ZWxvcGVyLzk2NWU0ZGI3LTU3YTMtM2FhYy1hYmNhLWE2NzEzODI5NWJiMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTUuMTg4LjQ3LjE4NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.-onaSw0J63JhTCBmAonb6ZokEhFDJHs12GD5h8giJ7Y023oCzv0NJq0DqDxefNlfdo91c_iWAth1OF6U787fKA
```
#### Decoded
##### Header
```json
{
  "typ": "JWT",
  "alg": "HS512",
  "kid": "28a318f7-0000-a1eb-7fa1-2c7433c6cca5"
}
```
##### Payload
```json
{
  "iss": "supercell",
  "aud": "supercell:gameapi",
  "jti": "0b9817c9-b2fe-4fed-bf8d-327ee1834970",
  "iat": 1630600600,
  "sub": "developer/965e4db7-57a3-3aac-abca-a67138295bb2",
  "scopes": [
    "brawlstars"
  ],
  "limits": [
    {
      "tier": "developer/silver",
      "type": "throttling"
    },
    {
      "cidrs": [
        "15.188.47.187"
      ],
      "type": "client"
    }
  ]
}
```
##### Signature
The signature is composed of three elements:
- Header
- Payload
- Secret

```python
HMACSHA512(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  your-256-bit-secret
)
```

#### Ressources
According to https://developer.brawlstars.com/#/documentation (account might be require), there is 5 available ressources:
- ```Players```: Access player specific information
- ```Clubs```: Access club specific information
- ```Rankings```: Access global and local rankings
- ```Brawlers```: Access general brawler information
- ```Events```

This project will use ```players``` data from ```rankings``` to create tier-list for current ```events```.

Thus, three ressources will be used:
- ```Players```
- ```Rankings```
- ```Events```

## Retreive top player's data
### Process flow
```Get leaderboard``` ➔ ```Extract player's tags``` ➔ ```Get battlelogs of each player```

### Ranking data structure
For sake of readability, data structure is represented in YAML:
```yaml
---
items:
- tag: "#2VQ82YGY"
  name: TwistiTwik
  nameColor: '0xffff8afb'
  icon:
    id: 28000073
  trophies: 59499
  rank: 1
  club:
    name: A Few Good Men
- tag: "#298LY8009"
  name: Que Pasa Asap
  nameColor: '0xff1ba5f5'
  icon:
    id: 28000008
  trophies: 51547
  rank: 2
  club:
    name: A Few Good Men
[...]
- tag: "#VY0Y20PQ"
  name: Raid
  nameColor: '0xfff05637'
  icon:
    id: 28000023
  trophies: 41955
  rank: 200
  club:
    name: CHICAGO BULLS
paging:
  cursors: {}
...
```
### Players data structure
⚠ Winner is not always in the first team (here the tag used was ```#2VQ82YGY```).
```yaml
---
items:
- battle:
    teams:
    - - tag: "#UV9Q9VJJ"
        name: "BIG | Eqwaak\U0001F986"
        brawler:
          trophies: 814
          id: 16000001
          power: 10
          name: COLT
      - tag: "#298LY8009"
        name: Que Pasa Asap
        brawler:
          trophies: 906
          id: 16000050
          power: 10
          name: GRIFF
      - tag: "#2VQ82YGY"
        name: TwistiTwik
        brawler:
          trophies: 1072
          id: 16000015
          power: 10
          name: PIPER
    - - tag: "#C9PU2L9L"
        name: Kaioken Goku
        brawler:
          trophies: 957
          id: 16000017
          power: 10
          name: TARA
      - tag: "#8R0GPL8QU"
        name: Dr.cool
        brawler:
          trophies: 922
          id: 16000010
          power: 10
          name: EL PRIMO
      - tag: "#R2CYV9UP"
        name: Brawl Master
        brawler:
          trophies: 972
          id: 16000047
          power: 10
          name: SQUEAK
    mode: brawlBall
    duration: 102
    type: ranked
    starPlayer:
      tag: "#C9PU2L9L"
      name: Kaioken Goku
      brawler:
        trophies: 957
        id: 16000017
        power: 10
        name: TARA
    trophyChange: -11
    result: defeat
  battleTime: 20210905T030043.000Z
  event:
    map: Slalom Slam
    id: 15000162
    mode: brawlBall
[...]
paging:
  cursors: {}
...
```
### Events data structure
## Player's data processing
### Process flow
```Get GEM GRAB battlelogs only``` ➔ ```Identify winning team for each battle``` ➔ ```Print out the most winning team```

Three outputs are possible:
- __Solo queue__: the most-winning brawler, no matter the two other brawlers withing the team
- __Duo queue__: the most-winning brawler peer, no matter the last brawler within the team
- __Trio queue__: the most-winning brawler trio


## Results
TBD


## Working environment
### Network diagram
![image](https://user-images.githubusercontent.com/28600326/132100796-b649801a-9732-40bd-ba50-91907e18ecb3.png)

### AWS VM
To connect to the AWS EC2 instance, you need:
- An SSH client
- The EC2 "brawl-star-api.pem" RSA key

Use the following command to access to the AWS EC2 instance:
```
ssh -i "brawl-star-api.pem" ec2-user@ec2-15-188-47-187.eu-west-3.compute.amazonaws.com
```

You should enter into the following shell:
![image](https://user-images.githubusercontent.com/28600326/131877713-990a8a5f-8dba-4e98-b9cf-c033a0c3b2c6.png)
> Note: This instance is free of charge while respecting some performance restriction.

### Python
#### Version
```
[ec2-user@ip-172-31-45-183 ~]$ python -V
Python 2.7.18
```

#### Libraries

### API
The API used in this project is the offical Supercell Brawl Star API that you can find here https://developer.brawlstars.com/#/,

To use it, first create an account, and then bind it to an API token that you create here: https://developer.brawlstars.com/#/new-key

![image](https://user-images.githubusercontent.com/28600326/131879099-3dfdae3e-08e0-4cd1-b412-36101d9749fc.png)
> Note: Replace X.X.X.X with your public IP address that you can find here: http://www.mon-ip.com/

Below is the output of the successfully created key:
![image](https://user-images.githubusercontent.com/28600326/131879625-aa300953-3e75-45b8-b228-cd8f0bf93a95.png)


Then, use it in the following code to GET content (code snipet generated by Postman and stored in api.py):
```python
import requests

url = "https://api.brawlstars.com/v1/rankings/FR/players"

payload={}
headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImU5MjY2ZTY3LTllYzQtNGE1OS1hNjAzLTA0ZTc4YWY5ZGRjYSIsImlhdCI6MTYzMDU5OTE4Mywic3ViIjoiZGV2ZWxvcGVyLzk2NWU0ZGI3LTU3YTMtM2FhYy1hYmNhLWE2NzEzODI5NWJiMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTA5LjI0LjIxOS4xMjUiXSwidHlwZSI6ImNsaWVudCJ9XX0.vgNoq2Jr9X1kLJvvvRxiEG_zZjSFuNihkmhOQiHtSvUW6UZUwrsjYSVvTazclJDRIXnC98TNkXhKtJQso1HMeg'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

```
Command
```
[ec2-user@ip-172-31-45-183 brawl-tier]$ python api.py
```

## Data structure
### Battlelog
```json
{
      "battleTime": "20210902T175027.000Z",
      "event": {
        "id": int,
        "mode": string,
        "map": string
      },
      "battle": {
        "mode": string,
        "type": string,
        "result": string,
        "duration": int,
        "trophyChange": int,
        "starPlayer": {
          "tag": string,
          "name": string,
          "brawler": {
            "id": int,
            "name": string,
            "power": int,
            "trophies": int
          }
        },
        "teams": [
          [
            {
              "tag": string,
              "name": string,
              "brawler": {
                "id": int,
                "name": string,
                "power": int,
                "trophies": int
              }
            },
            {
              "tag": string,
              "name": string,
              "brawler": {
                "id": int,
                "name": string,
                "power": int,
                "trophies": int
              }
            },
            {
              "tag": string,
              "name": string,
              "brawler": {
                "id": int,
                "name": string,
                "power": int,
                "trophies": int
              }
            }
          ],
          [
            {
              "tag": string,
              "name": string,
              "brawler": {
                "id": int,
                "name": string,
                "power": int,
                "trophies": int
              }
            },
            {
              "tag": string,
              "name": string,
              "brawler": {
                "id": int,
                "name": string,
                "power": int,
                "trophies": int
              }
            },
            {
              "tag": string,
              "name": string,
              "brawler": {
                "id": int,
                "name": string,
                "power": int,
                "trophies": int
              }
            }
          ]
        ]
      }
    }
```
### Ranking
```json
{
  "tag":string,
  "name":string,
  "nameColor":string,
  "icon":
  {
    "id":int
  },
  "trophies":int,
  "rank":int,
  "club":{
    "name":string
  }
}
```

### YAML
![image](https://user-images.githubusercontent.com/28600326/132695100-1d18d106-70ba-4fc0-9c33-7683c9a13b11.png)
