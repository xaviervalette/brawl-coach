# brawl-tier
Extract brawl star top tier from players data.

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
[
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
Output
```
{"items":[{"tag":"#2VQ82YGY","name":"TwistiTwik","nameColor":"0xffff8afb","icon":{"id":28000029},"trophies":57124,"rank":1,"club":{"name":"A Few Good Men"}},{"tag":"#8LQ9JR82","name":"BIG | Eqwaak🦆","nameColor":"0xffff8afb","icon":{"id":28000004},"trophies":48266,"rank":2,"club":{"name":"A Few Good Men"}},{"tag":"#9P2G9R2V","name":"EP|Evan","nameColor":"0xffff8afb","icon":{"id":28000041},"trophies":47338,"rank":3,"club":{"name":"CraZe Clan"}},{"tag":"#2V9G8L80","name":"I hate randoms","nameColor":"0xffffffff","icon":{"id":28000014},"trophies":47251,"rank":4,"club":{"name":"Prᴏᴠᴏᴄᴀᴛɪᴏɴ™"}},{"tag":"#G99CYGL","name":"CallMeZaiko☃️","nameColor":"0xff4ddba2","icon":{"id":28000011},"trophies":47148,"rank":5,"club":{"name":"TreborVGX"}},{"tag":"#G0JLPR8P","name":"Angry Boss 😡","nameColor":"0xffcb5aff","icon":{"id":28000014},"trophies":47132,"rank":6,"club":{"name":"Moonlight"}},{"tag":"#2GVY09J2","name":"mat the c@tz","nameColor":"0xff1ba5f5","icon":{"id":28000072},"trophies":46748,"rank":7,"club":{"name":"TreborVGX"}},{"tag":"#9GQGJJ0V","name":"Vałtłeman🕊","nameColor
":"0xff1ba5f5","icon":{"id":28000072},"trophies":46684,"rank":8,"club":{"name":"Adulte France"}},{"tag":"#QY92R8JU","name":"地|A_polocreed🎋","nameColor":"0xff1ba5f5","icon":{"id":28000014},"trophies":46497,"rank":9,"club":{"name":"Monarchy 🐐"}},{"tag":"#P8JPCLR","name":"Lord","nameColor":"0xff1ba5f5","icon":{"id":28000014},"trophies":46439,"rank":10,"club":{"name":"MBC Esports"}},{"tag":"#9QVQCLGL","name":"ZER | βεΙzεβυth","nameColor":"0xffcb5aff","icon":{"id":28000044},"trophies":46408,"rank":11,"club":{"name":"TreborVGX"}},{"tag":"#28VYUG9C2","name":"LaWin❤️🔥✨","nameColor":"0xffff8afb","icon":{"id":28000073},"trophies":46280,"rank":12,"club":{"name":"AFGM GENESIS"}},{"tag":"#Q0GR8Q8J","name":"YT: GreGouZz™☣","nameColor":"0xffffffff","icon":{"id":28000010},"trophies":46021,"rank":13,"club":{"name":"TreborVGX"}},{"tag":"#99982RQG","name":"C҉A҉R҉¥✨°","nameColor":"0xff1ba5f5","icon":{"id":28000067},"trophies":45710,"rank":14,"club":{"name":"TreborVGX"}},{"tag":"#20L20PL9Q","name":"OF | Gum","nameColor":"0xffcb5aff","icon":{"id":28000014},"trophies":45572,"rank":15,"club":{"name":"✨<c6>Jusт</c>30"}},{"tag":"#298LY8009","name":"Que Pasa Asap","nameColor":"0xff1ba5f5","icon":{"id":28000008},"trophies":45536,"rank":16,"club":{"name":"A Few Good Men"}},{"tag":"#8VCY2JYYR","name":"聚Yass☔","nameColor":"0xffffffff","icon":{"id":28000066},"trophies":45360,"rank":17,"club":{"name":"MBC Esports"}},{"tag":"#LLU0CYYL","name":"Mathieu","nameColor":"0xffa2e3fe","icon":{"id":28000071},"trophies":45342,"rank":18,"club":{"name":"SandStorm 🌪"}},{"tag
":"#2QC8VJ2","name":"⛩|Rzm64🎋","nameColor":"0xfff05637","icon":{"id":28000014},"trophies":45285,"rank":19,"club":{"name":"A Few Good Men"}},{"tag":"#9P9YRPRJU","name":"Ethaninho","nameColor":"0xffff9727","icon":{"id":28000038},"trophies":45285,"rank":20,"club":{"name":"AFGM GENESIS"}},{"tag":"#RQGUGYG0","name":"💮𝕊𝕚𝕞𝕠𝕟💮","nameColor     ":"0xffffce89","icon":{"id":28000039},"trophies":45161,"rank":21,"club":{"name":"MBC Esports"}},{"tag":"#PUVC9RQ","name":"Sparrow🥀","nameColor":"0xff4ddba2","icon":{"id":28000014},"trophies":44971,"rank":22,"club":{"name":"CHICAGO BULLS"}},{"tag":"#QPPV2VRV","name":"🍹|『ʟᴜᴄᴀꜱ⁸⁸⁸』🖤","nameColor":"0xffff8afb","icon":{"id":28000014},"trophies":44955,"rank":23,"club":{"name":"Etozya™"}},{"tag":"#GQUC0LGG","name":"Darkoum","nameColor":"0xffa2e3fe","icon":{"id":28000033},"trophies":44875,"rank":24,"club":{"name":"A Few Good Men"}},{"tag":"#2CPQU9C2L","name":"UP|mega🙃","nameColor":"0xffffffff","icon":{"id":28000044},"trophies":44765,"rank":25,"club":{"name":"CHICAGO BULLS"}},{"tag":"#PJCRL9QRY","name":"ϻaͥleͣkͫ ᴳᵒᵈ🃏","nameColor":"0xfff9c908","icon":{"id":28000018},"trophies":44719,"rank":26,"club":{"name":"Synergy™"}},{"tag":"#L92J8YR2","name":"Raswert ϟ","nameColor":"0xfff05637","icon":{"id":28000010},"trophies":44675,"rank":27,"club":{"name":"Hecho En México"}},{"tag":"#2V9PJYRP2","name":"🕊️|ᴷˡᵃʳⁱᵒⁿヅ","nameColor":"0xffffffff","icon":{"id":28000058},"trophies":445 72,"rank":28,"club":{"name":"TreborVGX"}},{"tag":"#20928GQ92","name":"九|Aziz 🐺","nameColor":"0xffffffff","icon":{"id":28000057},"trophies":44554,"rank":29,"club":{"name":"MBC Esports"}},{"tag":"#809R8JV8Q","name":"Glx|Tizzou🕊","nameColo r":"0xffffffff","icon":{"id":28000072},"trophies":44473,"rank":30,"club":{"name":"CHICAGO BULLS"}},{"tag":"#2GQYYVRR","name":"brn_nixerBoy","nameColor":"0xfff9c908","icon":{"id":28000038},"trophies":44447,"rank":31,"club":{"name":"nixer army"}},{"tag":"#8909GPC8P","name":"LM/adama28","nameColor":"0xff1ba5f5","icon":{"id":28000065},"trophies":44443,"rank":32,"club":{"name":"CHICAGO BULLS"}},{"tag":"#28YRULGUR","name":"Paul","nameColor":"0xfff9c908","icon":{"id":28000073},"trophies":44414,"rank":33,"club":{"name":"TreborVGX"}},{"tag":"#2VQV2CYJU","name":"Ethan","nameColor":"0xfff05637","icon":{"id":28000014},"trophies":44405,"rank":34,"club":{"name":"Mortis Gang"}},{"tag":"#2LL9G9LCQ","name":"RG|Nat","nameColor":"0xff1ba5f5","icon":{"id":28000072},"trophies":44354,"rank":35,"club":{"name":"Royale Gaming"}},{"tag":"#JVR2J9Q","name":"AK|hisoka","nameColor":"0xff1ba5f5","icon":{"id":28000007},"trophies":44346,"rank":36,"club":{"name":"Dark Team"}},{"tag":"#82U92202C","name":"Neyjīn⚘","nameColor":"0xffcb5aff","icon":{"id":28000014},"trophies":44101,"rank":37},{"tag":"#PQUPJQRGJ","name":"ιχ|мєн𝖆ℓℓι7🥀","nameColor":"0xffffffff","icon":{"id":28000044},"trophies":44048,"rank":38,"club":{"na me":"WSA"}},{"tag":"#8CQ0YULP","name":"WSA☠️Fury Noc☠️","nameColor":"0xffff9727","icon":{"id":28000014},"trophies":44011,"rank":39,"club":{"name":"WSA"}},{"tag":"#G2JQC0U","name":"Toinoumc 🃏","nameColor":"0xff1ba5f5","icon":{"id":28000072},"trophies":43996,"rank":40,"club":{"name":"A Few Good Men"}},{"tag":"#2PP2UG88Y","name":"🖤|Dɾαɠσɳҽᴳᵒᵈ⛓️","nameColor":"0xff1ba5f5","icon":{"id":28000004},"trophies":43982,"rank":41,"club":{"name":"✨<c6>Jusт</c>30"}},{"tag":"#8290YRCJ9","name":"Ytb|~JugWate~🥀","nameColor":"0xff4ddba2","icon":{"id":28000072},"trophies":43943,"rank":42,"club":{"name":"Munich Warriors"}},{"tag":"#Y2VLRLGP","name":"εтнαη ♡︎","nameColor":"0xffffffff","icon":{"id":28000073},"trophies":43933,"rank":43,"club":{"name":"Monarchy 🐐"}},{"tag":"#80UP00GQ9","name":"WSG | LeCookie™","nameColor":"0xffff8afb","icon":{"id":28000072},"trophies":43866,"rank":44,"club":{"name":"WSA"}},{"tag":"#8JCJCL0R9","name":"sholog","nameColor":"0xffcb5aff","icon":{"id":28000064},"trophies":43866,"rank":45},{"tag":"#QGQJYRY2","name":"Mᴿιβ👹","nameColor":"0xffff8afb","icon":{"id":28000073},"trophies":43850,"rank":46,"club":{"name":"MaîtreDuTemps🔮"}},{"tag":"#22U88JQ2Q","name":"nonoma'","nameColor":"0xffffffff","icon":{"id":28000042},"trophies":43849,"rank":47},{"tag":"#29L028GQL","name":"Djahsta","nameColor":"0xff1ba5f5","icon":{"id":28000004},"trophies":43832,"rank":48,"club":{"name":"Djalasta King"}},{"tag":"#Y029V0G9U","name":"あ|Whitax 🌺","nameColor":"0xffa2e3fe","icon":{"id":28000005},"trophies":43800,"rank":49,"club":{"name":"CHICAGO BULLS"}},{"tag":"#U0PYY0JU","name":"␈❥𝑅𝑖𝑦𝑎𝑛☯︎︎","nameColor":"0xffa2e3fe","icon":{"id":28000072},"trophies":43798,"rank":5     0,"club":{"name":"Synergy™"}},{"tag":"#G8LQRU9Y","name":"øCe | Ƶeησχ☄️","nameColor":"0xffff9727","icon":{"id":28000038},"trophies":43773,"rank":51,"club":{"name":"Océanik E-Sport"}},{"tag":"#2LLJQPC0P","name":"Łyrəm🥜ᶜᵃᶜᵃʰᵘᵉᵗ","nameColor":"0xffcb5aff","icon":{"id":28000014},"trophies":43749,"rank":52},{"tag":"#2JJJLG9G","name":"BaskiŁŁer","nameColor":"0xffa2e3fe","icon":{"id":28000073},"trophies":43742,"rank":53},{"tag":"#L8P90LPL","name":"あ|Yøuman 🦋","nameColor":"0xffcb5aff","icon":{"id":28000065},"trophies":43675,"rank":54,"club":{"name":"L’ÉTOILE ROUGE"}},{"tag":"#Y99L9L8","name":"Happy","nameColor":"0xff1ba5f5","icon":{"id":28000004},"trophies":43665,"rank":55,"club":{"name":"MBC Esports"}},{"tag":"#29JG9G8JY","name":"jojo.DU 21⚽","nameColor":"0xff4ddba2","icon":{"id":28000019},"trophies":43587,"rank":56,"club":{"name":"CHICAGO BULLS"}},{"tag":"#9908U9QGV","name":"Wetz_BS","nameColor":"0xffa2e3fe","icon":{"id":28000053},"trophies":43548,"rank":57,"club":{"name":"FrenchEmpire🖤"}},{"tag":"#90J2YJGQ","name":"🏆ＬｅＰｉｚｚａＦｏｕ✰","nameColor":"0xffa2e3fe","icon":{"id":28000073},"trophies":43544,"rank":58},{"tag":"#8LYUR2R2Q","name":"余 | ßαçøッ","nameColor":"0xff4ddba2","icon":{"id":28000011},"trophies":43511,"rank":59,"club":{"name":"Synergy™"}},{"tag":"#2QVYVP8U8","name":"brody","nameColor":"0xfff05637","icon":{"id":28000037},"trophies":43511,"rank":60,"club":{"name":"New SD player"}},{"tag":"#2J90GGLQU","name":"德|Z҉🅰︎🇨 Ҝ🥀ᵒᵖ
","nameColor":"0xff4ddba2","icon":{"id":28000013},"trophies":43504,"rank":61},{"tag":"#P9J9J8JU8","name":"火|Hatim🦆","nameColor":"0xffff8afb","icon":{"id":28000073},"trophies":43424,"rank":62,"club":{"name":"Adri7NeLuZz"}},{"tag":"#2809JJYVQ","name":"♨Denss♨","nameColor":"0xffff9727","icon":{"id":28000006},"trophies":43424,"rank":63,"club":{"name":"CHICAGO BULLS"}},{"tag":"#2P8GGV9LJ","name":"ECL | shao","nameColor":"0xff1ba5f5","icon":{"id":28000059},"trophies":43418,"rank":64,"club":{"name":"Neverland"}},{"tag":"#2YU9RPPQP","name":"🍭ᴀʟᴇxɪꜱ₁₀","nameColor":"0xff1ba5f5","icon":{"id":28000029},"trophies":43401,"rank":65,"club":{"name":"Adri7NeLuZz"}},{"tag":"#LV9PLGG","name":"MCES Mamat","nameColor":"0xff1ba5f5","icon":{"id":28000065},"trophies":43383,"rank":66,"club":{"name":"A Few Good Men"}},{"tag":"#2JJ8L2QYQ","name":"メS͎ᴘi̶ᴅe̸ʀ🕸","nameColor":"0xffcb5aff","icon":{"id":28000072},"trophies":43232,"rank":67,"club":{"name":" 30🎅"}},{"tag":"#C280UUUU","name":"GOD |🎋charmand","nameColor":"0xfff9775d","icon":{"id":28000073},"trophies":43223,"rank":68,"club":{"name":"CHICAGO BULLS"}},{"tag":"#80V80J8Y8","name":"ƦNS|Boubou⁶⁹🐨","nameColor":"0xffffffff","icon":{"id":28000063},"trophies":43206,"rank":69,"club":{"name":"<c7>Hitmen♡</c>"}},{"tag":"#2LYQJL0V2","name":"Ƭωєєкσ™✨","nameColor":"0xffffffff","icon":{"id":28000073},"trophies":43171,"rank":70,"club":{"name":"CHICAGO BULLS"}},{"tag":"#2YRCQR89U","name":"🍂🐿i ᴡᴏɴˡˢ�
🍂"","nameColor":"0xff4ddba2","icon":{"id":28000008},"trophies":43162,"rank":71,"club":{"name":"MBC Esports"}},{"tag":"#289VGLP","name":"Achille","nameColor":"0xfff9775d","icon":{"id":28000013},"trophies":43060,"rank":72},{"tag":"#2U0GYRRG","name":"Samjj","nameColor":"0xff4ddba2","icon":{"id":28000067},"trophies":43012,"rank":73,"club":{"name":"CHICAGO BULLS"}},{"tag":"#PY0PQ90QU","name":"aigledor","nameColor":"0xff1ba5f5","icon":{"id":28000043},"trophies":43010,"rank":74,"club":{"name":"Synergy™"}},{"tag":"#RJQ0822","name":"✨Diox ™️","nameColor":"0xffff8afb","icon":{"id":28000073},"trophies":42979,"rank":75,"club":{"name":"UN| French game"}},{"tag":"#9G2U8RJ8","name":"Ytb|IdhemBS❀","nameColor":"0xfff05637","icon":{"id":28000072},"trophies":42978,"rank":76,"club":{"name":"CODE : TACTIQUE"}},{"tag":"#2C2P8RYJ","name":"Rhum1™","nameColor":"0xffffffff","icon":{"id":28000073},"trophies":42959,"rank":77,"club":{"name":"Team LAZR"}},{"tag":"#22JUL8UR8","name":"6ix9ine","nameColor":"0xff1ba5f5","icon":{"id":28000037},"trophies":42937,"rank":78,"club":{"name":"Synergy™"}},{"tag":"#898YJCR9J","name":"DศffyDʊςkᴳᵒᵈツ","nameColor":"0xfff05637","icon":{"id":28000004},"trophies":42926,"rank":79,"club":{"name":"✨<c6>Jusт</c>30"}},{"tag":"#2PL898P29","name":"TS /noa","nameColor":"0xffa2e3fe","icon":{"id":28000036},"trophies":42872,"rank":80,"club":{"name":"CHICAGO BULLS"}},{"tag":"#GGPUPQRL","name":"Mr.Nedow🦆","nameColor":"0xffa2e3fe","icon":{"id":28000073},"trophies":42825,"rank":81,"club":{"name":"A Few Good Men"}},{"tag":"#RYGCVRL2","name":"Ksh🐧","nameColor":"0xffffffff","icon":{"id":28000073},"trophies":42758,"rank":82,"club":{"name":"Apollon Corp."}},{"tag":"#V2Q080UU","name":"☆TTB|Valembeau☆","nameColor":"0xff1ba5f5","icon":{"id":28000008},"trophies":42757,"rank":83,"club":{"name":"CHICAGO BULLS"}},{"tag":"#R8CQLV8","name":"wlad","nameColor":"0xffffffff","icon":{"id":28000003},"trophies":42747,"rank":84,"club":{"name":"A Few Good Men"}},{"tag":"#990U89200","name":"F2S|ϻα͢͢͢X🀄","nameColor":"0xffff8afb","icon":{"id":28000046},"trophies":42741,"rank":85,"club":{"name":"Foot2Stars"}},{"tag":"#2QL8P9UUY","name":"ᴳᵒᵈ乡ᴩᴏᴩ€y❤ʸᵒᵘツ","nameColor":"0xffa2e3fe","icon":{"id":28000026},"trophies":42717,"rank":86,"club":{"name":"PlayerShowdown¹"}},{"tag":"#8GLV20LGV","name":"$haĐøw","nameColor":"0xffff9727","icon":{"id":28000073},"trophies":42706,"rank":87,"club":{"name":"Møøn of Wølfs"}},{"tag":"#2U2QU0GVC","name":"ZPAM","nameColor":"0xffffffff","icon":{"id":28000073},"trophies":42705,"rank":88,"club":{"name":"MBC Esports"}},{"tag":"#P8CJU9L","name":"вa∂вoу 🦋","nameColor":"0xffffffff","icon":{"id":28000018},"trophies":42703,"rank":89,"club":{"name":"MBC Esports"}},{"tag":"#2JYLPPQ0R","name":"<[TX]>remtho74","nameColor":"0xffff9727","icon":{"id":28000016},"trophies":42698,"rank":90,"club":{"name":"MBC Esports"}},{"tag":"#PPUPUUJ","name":"AEL | Aiden ❤","nameColor":"0xffff8afb","icon":{"id":28000044},"trophies":42681,"rank":91,"club":{"name":"<c9>ᴀᴇʟʏᴀ</c>"}},{"tag":"#Y2YCJY","name":"ProFr","nameColor":"0xfff05637","icon":{"id":28000055},"trophies":42659,"rank":92,"club":{"name":">.<"}},{"tag":"#Y99Y2CUV","name":"🃏|ᴵ'ᵐ ηєяσχχ⛩️","nameColor":"0xfff9c908","icon":{"id":28000073},"trophies":42651,"rank":93,"club":{"name":"Invizibilation"}},{"tag":"#2VYJ00PG8","name":"Dannette66","nameColor":"0xffff9727","icon":{"id":28000073},"trophies":42645,"rank":94,"club":{"name":"CHICAGO BULLS"}},{"tag":"#2J2UJJRJ","name":"XV⚡GAMER ♨️","nameColor":"0xffa8e132","icon":{"id":28000059},"trophies":42616,"rank":95,"club":{"name":"♣️Just skill♣️"}},{"tag":"#G2Q2UY8G","name":"�ƒƒℓοοοοο🔥","nameColor":"0xffff9727","icon":{"id":28000017},"trophies":42592,"rank":96,"club":{"name":"CHICAGO BULLS"}},{"tag":"#2Y2Q2PP8C","name":"Faxe Valentin","nameColor":"0xffcb5aff","icon":{"id":28000034},"trophies":42523,"rank":97,"club":{"name":"Synergy™"}},{"tag":"#89UJY8CC2","name":"Lᴇᴇǫzi","nameColor":"0xffa2e3fe","icon":{"id":28000072},"trophies":42503,"rank":98,"club":{"name":"CHICAGO BULLS"}},{"tag":"#PQ8PQRJ","name":"🎑Finau >.<","nameColor":"0xff1ba5f5","icon":{"id":28000072},"trophies":42497,"rank":99,"club":{"name":"BlackBull ST™"}},{"tag":"#29LJP28VJ","name":"QLS | ArkOos","nameColor":"0xff1ba5f5","icon":{"id":28000072},"trophies":42482,"rank":100},{"tag":"#2YULVL8CY","name":"Hidan ᴷᴿᴵᴹ","nameColor":"0xff1ba5f5","icon":{"id":28000066},"trophies":42469,"rank":101},{"tag":"#J0PJVGQJ","name":"🦋・☆TTB|Théo☆","nameColor":"0xff1ba5f5","icon":{"id":28000034},"trophies":42461,"rank":102,"club":{"name":"CHICAGO BULLS"}},{"tag":"#V98VYQPJ","name":"Blutengei","nameColor":"0xffcb5aff","icon":{"id":28000073},"trophies":42447,"rank":103,"club":{"name":"L'équipage 🐬"}},{"tag":"#PJ0GRPR8","name":"支|xEyal⚡️","nameColor":"0xffffffff","icon":{"id":28000005},"trophies":42374,"rank":104,"club":{"name":"Follow ♥️"}},{"tag":"#2YYVYLVYU","name":"Kirito","nameColor":"0xffffffff","icon":{"id":28000073},"trophies":42366,"rank":105,"club":{"name":"Stay cool🍻"}},{"tag":"#9V09CCLUC","name":"Paul.crz","nameColor":"0xffff9727","icon":{"id":28000018},"trophies":42322,"rank":106,"club":{"name":"Adri7NeLuZz"}},{"tag":"#2GYRJ2GQL","name":"BS Eris JR","nameColor":"0xfff9c908","icon":{"id":28000073},"trophies":42321,"rank":107,"club":{"name":"Funleddy B"}},{"tag":"#2LRVPYC9","name":"Aizen is back🥀","nameColor":"0xffff8afb","icon":{"id":28000029},"trophies":42282,"rank":108,"club":{"name":"MBC Esports"}},{"tag":"#UGYVLRCP","name":"爆Kâtchân💣","nameColor":"0xfff05637","icon":{"id":28000072},"trophies":42278,"rank":109,"club":{"name":"Lakers United"}},{"tag":"#80VG9RV8V","name":"TDB |⛩ ©️〽️oi ⛩","nameColor":"0xff4ddba2","icon":{"id":28000010},"trophies":42271,"rank":110,"club":{"name":"CHICAGO BULLS"}},{"tag":"#9P8C22JG","name":"UNI|Hellay🐣","nameColor":"0xffffffff","icon":{"id":28000006},"trophies":42268,"rank":111,"club":{"name":"Unima Gaming"}},{"tag":"#22LQ0PV20","name":"⚠️♥️ferank ♥️⚠️","nameColor":"0xfff05637","icon":{"id":28000004},"trophies":42267,"rank":112},{"tag":"#LQ90UR8L","name":"千ɪɴᴀʟ|乃ᴏss","nameColor":"0xfff05637","icon":{"id":28000073},"trophies":42249,"rank":113,"club":{"name":"Synergy™"}},{"tag":"#9J0J2QP8Y","name":"chat team","nameColor":"0xfff9c908","icon":{"id":28000017},"trophies":42245,"rank":114,"club":{"name":"Layan_tv"}},{"tag":"#282L20GYU","name":"ØS|S̷h̷ɇɨ","nameColor":"0xffcb5aff","icon":{"id":28000014},"trophies":42242,"rank":115,"club":{"name":"CHICAGO BULLS"}},{"tag":"#29UGVPUCU","name":"FE|Hélicoptère","nameColor":"0xffff9727","icon":{"id":28000073},"trophies":42197,"rank":116,"club":{"name":"Synergy™"}},{"tag":"#98RVQPJ","name":"🃏|FéeNeMoney","nameColor":"0xffff8afb","icon":{"id":28000051},"trophies":42188,"rank":117},{"tag":"#2P0JJ809L","name":"jeredoubler","nameColor":"0xffff9727","icon":{"id":28000073},"trophies":42186,"rank":118,"club":{"name":"Pandou ESPORT"}},{"tag":"#88G20UULP","name":"WSA |ᵐⁱⁿⁱA҉obo҉","nameColor":"0xffcb5aff","icon":{"id":28000002},"trophies":42171,"rank":119},{"tag":"#20P0CGPRP","name":"blanc de dinde","nameColor":"0xfff05637","icon":{"id":28000016},"trophies":42154,"rank":120,"club":{"name":"CHICAGO BULLS"}},{"tag":"#LUVG889P","name":"👽","nameColor":"0xffcb5aff","icon":{"id":28000029},"trophies":42141,"rank":121,"club":{"name":"MBC Esports"}},{"tag":"#20QYPU9VY","name":"Gianni 🥺🍁 ","nameColor":"0xffffffff","icon":{"id":28000014},"trophies":42129,"rank":122,"club":{"name":"Follow ♥️"}},{"tag":"#YP0GVJ9","name":"OnRails|Clem","nameColor":"0xff1ba5f5","icon":{"id":28000062},"trophies":42126,"rank":123,"club":{"name":"OnRails"}},{"tag":"#2828VQ2Q9","name":"OWEE|mael0509","nameColor":"0xffa8e132","icon":{"id":28000068},"trophies":42126,"rank":124,"club":{"name":"PlayerShowdown¹"}},{"tag":"#Y2J0Y298","name":"★Grano★","nameColor":"0xffffffff","icon":{"id":28000020},"trophies":42116,"rank":125,"club":{"name":"AFGM GENESIS"}},{"tag":"#82Q00UGY","name":"laxus🥀","nameColor":"0xffffffff","icon":{"id":28000058},"trophies":42077,"rank":126,"club":{"name":"MBC Esports TR"}},{"tag":"#Q808R2CV","name":"☆TTB|Nestorツ☆","nameColor":"0xff1ba5f5","icon":{"id":28000060},"trophies":42073,"rank":127,"club":{"name":"CHICAGO BULLS"}},{"tag":"#29UYVQRQR","name":"Mermeud","nameColor":"0xffffffff","icon":{"id":28000010},"trophies":42062,"rank":128,"club":{"name":"New Dawn"}},{"tag":"#8PCJRLV8","name":"🕊️I9I🕊️","nameColor":"0xffcb5aff","icon":{"id":28000018},"trophi  es":42062,"rank":129,"club":{"name":"CHICAGO BULLS"}},{"tag":"#9UJYU9P92","name":"ØS | ғяσsт ﷼|❄️","nameColor":"0xffa2e3fe","icon":{"id":28000063},"trophies":42060,"rank":130,"club":{"name":"<c3>NewStar</c>"}},{"tag":"#98CRGCJLY","name":"TT henokstag","nameColor":"0xff1ba5f5","icon":{"id":28000073},"trophies":42052,"rank":131,"club":{"name":"Barleys Brewery"}},{"tag":"#VU0QRL9","name":"Cursed|Bat 🥺","nameColor":"0xffa2e3fe","icon":{"id":28000051},"trophies":42049,"rank":132, "club":{"name":"Perd<c8>u</c>"}},{"tag":"#UL8QC98","name":"LAZR|Rolex⚡️","nameColor":"0xfff9c908","icon":{"id":28000061},"trophies":42045,"rank":133,"club":{"name":"A Few Good Men"}},{"tag":"#P8RQPQ922","name":"clo-xploz","nameColor":"0xfff05637","icon":{"id":28000073},"trophies":42008,"rank":134,"club":{"name":"CHICAGO BULLS"}},{"tag":"#2VJ9G9QLR","name":"额|𝐶ℎ𝑎𝑚𝑝𝑖💘","na
meColor":"0xffcb5aff","icon":{"id":28000062},"trophies":41991,"rank":135,"club":{"name":"Mystic One"}},{"tag":"#99Q0R9CU8","name":"squibbo","nameColor":"0xffcb5aff","icon":{"id":28000044},"trophies":41975,"rank":136,"club":{"name":"CHICAGO BULLS"}},{"tag":"#8JRYUUQU8","name":"Hi Im Thomas🕊️","nameColor":"0xffcb5aff","icon":{"id":28000014 },"trophies":41965,"rank":137,"club":{"name":"L’ÉTOILE ROUGE"}},{"tag":"#PJ80QG90U","name":"LucsOG","nameColor":"0xffffffff","icon":{"id":28000044},"trophies":41963,"rank":138,"club":{"name":"CHICAGO BULLS"}},{"tag":"#P82U2C90P","name":"★•シ︎CABRO'E🥀","nameColor":"0xfff05637","icon":{"id":28000048},"trophies":41962,"rank":139,"club":{"name":"La fine équipe"}},{"tag":"#88JUQQRU8","name":"ayyoub du 59","nameColor":"0xff1ba5f5","icon":{"id":28000016},"trophies":41946,"rank":140,"club":{"name":"妥|Esport"}},{"tag":"#2YJ0U8Y09","name":"ØS|Nelson","nameColor":"0xfff9775d","icon":{"id":28000019},"trophies":41944,"rank":141},{"tag":"#20299QLYU","name":"rr_spike","nameColor":"0xff1ba5f5","icon":{"id":28000071},"trophies":41924,"rank":142,"club":{"name":"CHICAGO BULLS"}},{"tag":"#2GU8Y82VU","name":"ND|OmaaR⁰⁵","nameColor":"0xff1ba5f5","icon":{"id":28000034},"trophies":41907,"rank":143,"club":{"name":"MAJisTraL"}},{"tag":"#2YRQC88R8","name":"YT |Rigame乂☯︎︎","nameColor":"0xffff9727","icon":{"id":28000073},"trophies":41905,"rank":144,"club":{"name":"Synergy™"}},{"tag":"#J2U8LPVJ","name":"⛩️|Pinoc64🎋","nameColor":"0xff1ba5f5","icon":{"id":28000003},"trophies":41888,"rank":145,"club":{"name":"WSA"}},{"tag":"#28C9PCUYR","name":"時|MTG🐍シ","nameColor":"0xfff9c908","icon":{"id":28000072},"trophies":41885,"rank":146,"club":{"name":"Yasien💕"}},{"tag":"#8G2URV929","name":"Millenium","nameColor":"0xffffffff","icon":{"id":28000021},"trophies":41829,"rank":147,"club":{"name":"MBC Esports TR"}},{"tag":"#2UGQ09UJP","name":"☄️loulou™️☄️","nameColor":"0xfff05637","icon":{"id":28000016},"trophies":41796,"rank":148,"club":{"name":"Slide Gang"}},{"tag":"#8GUUV0QLQ","name":"Beurre","nameColor":"0xfff9c908","icon":{"id":28000049},"trophies":41796,"rank":149,"club":{"name":"Synergy™"}},{"tag":"#VQ9JVRPU","name":"⚡️chatrapace⚡️","nameColor":"0xfff05637","icon":{"id":28000044},"trophies":41787,"rank":150,"club":{"name":"Adri7NeLuZz"}},{"tag":"#2LLGVCRP","name":"SX|Paulo_¥€¥","nameColor":"0xfff05637","icon":{"id":28000068},"trophies":41778,"rank":151,"club":{"name":"Synergy™"}},{"tag":"#8PLU0PV9Y","name":"CM | 🈵Alex🈯️","nameColor":"0xffff8afb","icon":{"id":28000065},"trophies":41777,"rank":152,"club":{"name":"VV eSport"}},{"tag":"#98VRCP2C","name":"BK | Lunch","nameColor":"0xffcb5aff","icon":{"id":28000073},"trophies":41768,"rank":153,"club":{"name":"AFGM GENESIS"}},{"tag":"#8QYP9VVY9","name":"🗡Ｊｏｓｈ６  ９ʸᵗ🗡","nameColor":"0xffcb5aff","icon":{"id":28000071},"trophies":41743,"rank":154,"club":{"name":"S helly/Tara R35"}},{"tag":"#9GV2VUJP","name":"FC | 0Storm ♨️","nameColor":"0xff4ddba2","icon":{"id":28000073},"trophies":41737,"rank":155,"club":{"name":"Just ranK🌩"}},{"tag":"#2CRRCPGV2","name":"玄|sweezy🎋","nameColor":"0xfff9c908","icon" :{"id":28000044},"trophies":41714,"rank":156,"club":{"name":"ReLord"}},{"tag":"#282UC8CVP","name":"ＭᴿCₒcₒ🍟🍭🥝","nameColor":"0xff4ddba2","icon":{"id":28000073},"trophies":41713,"rank":157,"club":{"name":"MaîtreDuTemps🔮"}},{"tag":"#88RJQJLP","name":"SкγĐαгКᵚᵃᵑᵗᵧₒᵤ☔","nameColor":"0xffffce89","icon":{"id":28000073},"trophies":41689,"rank":158,"club":{"name":"Prᴏᴠᴏᴄᴀᴛɪᴏɴ™"}},{"tag":"#992QQLYJ9","name":"Leo🌰ⁿᵒⁱˢᵉᵗᵗᵉ","nameColor":"0xfff9c908","icon":{"id":28000073},"trophies":41685,"rank":159,"club":{"name":"CHICAGO BULLS"}},{"tag":"#JPYQYL02","name":"UNI |Kuzan_TV","nameColor":"0xffff9727","icon":{"id":28000071},"trophies":41676,"rank":160,"club":{"name":"Unima Gaming"}},{"tag":"#2JLQCCL9R","name":"Hz |Mileno","nameColor":"0xffcb5aff","icon":{"id":28000054},"trophies":41675,"rank":161,"club":{"name":"Heroz 🎃"}},{"tag":"#92LP08L","name":"Ｊｏｔａ　♤","nameColor":"0xff1ba5f5","icon":{"id":28000018},"trophies":41671,"rank":162,"club":{"name":"MBC Esports TR"}},{"tag":"#8V2J0RLV","name":"あ|kazuto 🌊","nameColor":"0xfff9c908","icon":{"id":28000056},"trophies":41670,"rank":163,"club":{"name":"Invizibilation"}},{"tag":"#2L8Y08PCU","name":"prism_ichigo","nameColor":"0xffffffff","icon":{"id":28000044},"trophies":41627,"rank":164},{"tag":"#9VPJLVJLU","name":"ˢᵃᵈCHEAT™","nameColor":"0xffcb5aff","icon":{"id":28000073},"trophies":41625,"rank":165,"club":{"name":"El Fire Purple"}},{"tag":"#C8VCY0LJ","name":"{RoW} Mattéo56","nameColor":"0xffa2e3fe","icon":{"id":28000067},"trophies":41613,"rank":166,"club":{"name":"The X-Pendables"}},{"tag":"#202CGV2RC","name":"ƦNS|Siℓver⁶⁹🦥","nameColor":"0xff1ba5f5","icon":{"id":28000046},"trophies":41605,"rank":167,"club":{"name" :"Monarchy 🐐"}},{"tag":"#Q928UCV0","name":"乂υτοριεツ","nameColor":"0xfff05637","icon":{"id":28000004},"trophies":41592,"rank":168},{"tag":"#9GJYPJCYQ","name":"muslim","nameColor":"0xff1ba5f5","icon":{"id":28000014},"trophies":41591,"rank":169,"club":{"name":"BlackBull ST™"}},{"tag":"#PVV899YLL","name":"CM|Alpha_Evans","nameColor":"0xffffffff","icon":{"id":28000054},"trophies":41583,"rank":170,"club":{"name":"CM|Squad🔥"}},{"tag":"#8C08998","name":"ᴍᴅᴛ | Evox🐬🔥","nameColor":"0xff1ba5f5","icon":{"id":28000017},"trophies":41580,"rank":171,"club":{"name":"MaîtreDuTemps🔮"}},{"tag":"#Q9Y8UL0U","name":"Force 様","nameColor":"0xffffffff","icon":{"id":28000073},"trophies":41565,"rank":172,"club":{"name":"Free Win"}},{"tag":"#2LUPGQ8C","name":"MCES FK","nameColor":"0xffffffff","icon":{"id":28000004},"trophies":41537,"rank":173,"club":{"name":"A Few Good Men"}},{"tag":"#2PLVV0PPG","name":"NoNo ツ","nameColor":"0xff1ba5f5","icon":{"id":28000037},"trophies":41531,"rank":174,"club":{"name":"french origin"}},{"tag":"#28CGPYQ29","name":"⛩|Ice❄StøRm™","nameColor":"0xffffce89","icon":{"id":28000004},"trophies":41522,"rank":175,"club":{"name":"CHICAGO BULLS"}},{"tag":"#80Y80RQ9J","name":"H💗❤C","nameColor":"0xfff9c908","icon":{"id":28000042},"trophies":41519,"rank":176,"club":{"name":"「UℓτiᴍaτeMak£r✨"}},{"tag":"#8L8V9RL","name":"AEL | Hugzzz 🤍","nameColor":"0xffffffff","icon":{"id":28000023},"trophies":41505,"rank":177,"club":{" name":"<c5>ᴀᴇʟʏᴀ</c>"}},{"tag":"#VGGG02PG","name":"MH | 〽️ustang","nameColor":"0xffffffff","icon":{"id":28000014},"trophies":41463,"rank":178,"club":{"name":"UnionFrançaise"}},{"tag":"#PG8292YQ","name":"Tismo_YTB","nameColor":"0xfff9c908","icon":{"id":28000073},"trophies":41455,"rank":179,"club":{"name":"⚡️World Storm🌩"}},{"tag":"#99L090J9P","name":"Tis〽️a ","nameColor":"0xffcb5aff","icon":{"id":28000072},"trophies":41452,"rank":180,"club":{"name":"Layan_tv"}},{"tag":"#R0JVP8RU","name":"UNI|Risitas","nameColor":"0xffffffff","icon":{"id":28000047},"trophies":41433,"rank":181,"club":{"name":"Unima Gaming"}},{"tag":"#22CPJ8RYQ","name":"🍭Filou X","nameColor":"0xff4ddba2","icon":{"id":28000040},"trophies":41431,"rank":182,"club":{"name":"YT : frags_og"}},{"tag":"#8Q9C0GYJ0","name":"NuMeRo_2-JeJe","nameColor":"0xfff05637","icon":{"id":28000023},"trophies":41422,"rank":183,"club":{"name":"Op3v3Players🤗"}},{"tag":"#2JR9YJL28","name":"戈| Leͥgeͣnͫd™🃏","nameColor":"0xffff9727","icon":{"id":28000073},"trophies":41420,"rank":184,"club":{"name":"Synergy™"}},{"tag":"#9YGYQQJL","name":"FrB|Vico<Drako","nameColor":"0xff4ddba2","icon":{"id":28000016},"trophies":41398,"rank":185,"club":{"name":"FrenchBinks"}},{"tag":"#9QLRLV9","name":"FRT Mehmet","nameColor":"0xff1ba5f5","icon":{"id":28000072},"trophies":41387,"rank":186,"club":{"name":"CHICAGO BULLS"}},{"tag":"#9R2QVU","name":"²Paquitoo 🂱","nameColor":"0xffff8afb","icon":{"id": 28000023},"trophies":41380,"rank":187},{"tag":"#22JJRJPG2","name":"ᴵᵗˢ ϻ๖ϻ's ᴳᵒᵈ☔","nameColor":"0xffcb5aff","icon":{"id":28000020},"trophies":41372,"rank":188,"club":{"name":"CHICAGO BULLS"}},{"tag":"#8YVRCR2GJ","name":"🌺₮łⱤ₳🌺","nameColor":"0xffcb5aff","icon":{"id":28000070},"trophies":41372,"rank":189,"club":{"name":"Synergy™"}},{"tag":"#2JQUU9GVQ","name":"LED|Kaddiboite","nameColor":"0xfff9c908","icon":{"id":28000032},"trophies":41364,"rank":190,"club":{"name":"⚡️World Storm🌩"}},{"tag":"#2P
RPRVRRU","name":"☆TTB|Ty Saphir☆","nameColor":"0xffcb5aff","icon":{"id":28000036},"trophies":41362,"rank":191,"club":{"name":"CHICAGO BULLS"}},{"tag":"#8CP0QCLJY","name":"UP |『Ｔｏｘｙｚ』™️","nameColor":"0xfff05637","icon":{"id":28000073},"trophies":41358,"rank":192,"club":{"name":"FC Paydey"}},{"tag":"#UR00VPLQ","name":"Huang","nameColor":"0xfff9c908","icon":{"id":28000037},"trophies":41349,"rank":193,"club":{"name":"CHICAGO BULLS"}},{"tag":"#2P2JYYRP8","name":"FM | Ex4lTy☔™","nameColor":"0xffffffff","icon":{"id":28000032},"trophies":41343,"rank":194,"club":{"name":"CHICAGO BULLS"}},{"tag":"#PY0Q0G9R","name":"PS | iiSunn~🎩","nameColor":"0xffcb5aff","icon":{"id":28000018},"trophies":41343,"rank":195,"club":{"name":"PollyStirene"}},{"tag":"#LPR0UPU","name":"C'EST CIAO","nameColor":"0xff4ddba2","icon":{"id":28000049},"trophies":41343,"rank":196,"club":{"name":"Unima Gaming"}},{"tag":"#902LU0U0","name":"夜|Blirage🌖","nameColor":"0xfff9c908","icon":{"id":28000020},"trophies":41336,"rank":197,"club":{"name":"Mugiwara 👒"}},{"tag":"#29YV028CV","name":"FC|Miguel","nameColor":"0xff1ba5f5","icon":{"id":28000072},"trophies":41334,"rank":198,"club":{"name":"New Dawn"}},{"tag":"#29VYPP9GY","name":"🌬я4ιηﾒ","nameColor":"0xffffce89","icon":{"id":28000003},"trophies":41332,"rank":199},{"tag ":"#RRVVPG2Y","name":"🃏悲伤Brosta☄️>.<","nameColor":"0xff1ba5f5","icon":{"id":28000041},"trophies":41328,"rank":200,"club":{"name":"tontonflingueur"}}],"paging":{"cursors":{}}}
```