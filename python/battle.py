class Battle:
   

   def __init__(self, battle):
      self.noDuration=False
      self.noStarPlayer=False
      self.noResult=False
      self.noType=False
      self.noTeams=False
      self.noPlayers=False
      self.noStarBrawlerTrophies=False
      self.noStarBrawlerPower=False

      self.mode = battle['battle']['mode']
      if 'duration' in battle['battle']:
         self.duration = battle['battle']['duration']
      else:
         self.noDuration=True

      if 'type' in battle['battle']:
         self.typee = battle['battle']['type']
      else:
         self.noType=True
      
      if 'result' in battle['battle']:
         self.result = battle['battle']['result']   
      else:
         self.noResult=True

      if 'teams' in battle['battle']:
         self.teams=battle['battle']['teams']
      else:
         self.noTeams=True
      
      if 'players' in battle['battle']:
         self.players=battle['battle']['players']
      else:
         self.noPlayers=True

      self.battleTime=battle['battleTime']
      self.mapEvent=battle['event']['map']
      self.idEvent=battle['event']['id']
      self.modEvent=battle['event']['map']
      
      
      if 'starPlayer' in battle['battle'] and battle['battle']['starPlayer'] is not None :
         self.starTag=battle['battle']['starPlayer']['tag']
         self.starName=battle['battle']['starPlayer']['name']
         if 'trophies' in battle['battle']['starPlayer']['brawler']:
            self.starBrawlerTrophies=battle['battle']['starPlayer']['brawler']["trophies"]
         else:
            self.noStarBrawlerTrophies=True
         
         self.starBrawlerId=battle['battle']['starPlayer']['brawler']["id"]

         if 'power' in battle['battle']['starPlayer']['brawler']:
            self.starBrawlerPower=battle['battle']['starPlayer']['brawler']["power"]
         else:
            self.noStarBrawlerPower=True

         
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