class Battle:
   

   def __init__(self, battle):
      self.noDuration=False
      self.noStarPlayer=False
      self.noResult=False
      self.mode = battle['battle']['mode']
      if 'duration' in battle['battle']:
         self.duration = battle['battle']['duration']
      else:
         self.noDuration=True
      self.typee = battle['battle']['type']
      if 'result' in battle['battle']:
         self.result = battle['battle']['result']   
      else:
         self.noResult=True
      self.battleTime=battle['battleTime']
      self.mapEvent=battle['event']['map']
      self.idEvent=battle['event']['id']
      self.modEvent=battle['event']['map']
      self.teams=battle['battle']['teams']
      
      if 'starPlayer' in battle['battle'] and battle['battle']['starPlayer'] is not None :
         self.starTag=battle['battle']['starPlayer']['tag']
         print("star tag: ", self.starTag)
         self.starName=battle['battle']['starPlayer']['name']
         self.starBrawlerTrophies=battle['battle']['starPlayer']['brawler']["trophies"]
         self.starBrawlerId=battle['battle']['starPlayer']['brawler']["id"]
         self.starBrawlerPower=battle['battle']['starPlayer']['brawler']["power"]
         self.starBrawlername=battle['battle']['starPlayer']['brawler']["name"]
         self.winTeam=self.get_team_of_star_player()
      else:
         self.noStarPlayer= True

      
   def get_team_of_star_player(self):
      goodTeam=False
      winTeam=[]

      for team in self.teams:
         if goodTeam== False:
               winTeam.clear()
               for i in range(len(team)):
                  winTeam.append(team[i]["brawler"]["name"])
                  if team[i]["tag"]==self.starTag:
                     goodTeam=True
      winTeam.sort()
      return winTeam

   def is_equal(self, otherBattle):
      if self.duration==otherBattle.duration and self.battleTime==otherBattle.battleTime:
         return True
      else:
         return False