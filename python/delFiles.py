from os import walk
from functions import *

currentEvents=readCurrentEvents("todo")

filesList = []
for (dirpath, dirnames, filenames) in walk("../../data/battles/"):
    for filename in filenames:
        fn = filename.split("."); 
        oldEventNumber=int(fn[0])
        with open(dataPath+'/battles/'+filename, 'r') as f:
            old_battle=json.load(f)
        try:
            if old_battle[0]["event"]["id"]!=currentEvents[oldEventNumber]["event"]["id"]:
                try:
                    os.remove(dataPath+"/battles/"+str(oldEventNumber)+".json")
                except:
                    print("no file")
        except:
            os.remove(dataPath+"/battles/"+str(oldEventNumber)+".json")

