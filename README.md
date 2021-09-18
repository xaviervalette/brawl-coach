# <img src="https://user-images.githubusercontent.com/28600326/133853719-9c5c6942-89c8-42ef-bbb2-083f644cc824.png" width="20" height="20">  Brawl Stars - Brawler tiers from leaderboard analysis

- Brawl Stars REST API
- Retrieve player's information
- Process player's information

## Network diagram
<img width="100%" alt="Picture6" src="https://user-images.githubusercontent.com/28600326/133892580-82ad3563-11e9-433a-9db3-a80dbf5682b8.png">


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
🛈 For sake of clarity, JSON output will be printed as YAML. If you are not familiar with this data serialization language, please check https://yaml.org/.
```yaml
---
typ: JWT
alg: HS512
kid: 28a318f7-0000-a1eb-7fa1-2c7433c6cca5
...
```
##### Payload
```yaml
---
iss: supercell
aud: supercell:gameapi
jti: 0b9817c9-b2fe-4fed-bf8d-327ee1834970
iat: 1630600600
sub: developer/965e4db7-57a3-3aac-abca-a67138295bb2
scopes:
- brawlstars
limits:
- tier: developer/silver
  type: throttling
- cidrs:
  - 15.188.47.187
  type: client
...
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

### Ressources
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
- __Solo queue__: the most-winning brawler, regardless the two other brawlers withing the team
- __Duo queue__: the most-winning brawler peer, regardless the last brawler within the team
- __Trio queue__: the most-winning brawler trio


## Results
TBD
