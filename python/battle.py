class Battle:
   def __init__(self, battle):
      self.mode = battle['battle']['mode']
      self.duration = battle['battle']['duration']
      self.typee = battle['battle']['type']
      self.result = battle['battle']['result']   
      self.battleTime=battle['battleTime']
      self.mapEvent=battle['event']['map']
      self.idEvent=battle['event']['id']
      self.modEvent=battle['event']['map']