from itertools import product
from garch_utils.getList import getIndexList
import json


indexList = getIndexList(mode = 0)
sdList = [2]
dayList = [30,50,60,90,120]
paramList = list(product(sdList, dayList))
data = []
for index in indexList:
    entry = {
        "index": {
            "name": index,
            "parameter": []}
        
    }
    #print(entry["stock"])
    for (i,(SD,day)) in enumerate(paramList):
        entry["index"]["parameter"].append([{"SD": SD}, {"day": day}])
    #print(entry)
    data.append(entry)

with open('info/indexJson.json', 'w') as fp:
    json.dump(data, fp, indent=4)