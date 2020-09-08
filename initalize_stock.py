from itertools import product
from garch_utils.getList import getStockHKList
from garch_utils.getList import getStockUSList
import json

stocktype = "HK"
component = "HSI"

if stocktype == "US":
    stockList = getStockUSList(node = 0)
elif stocktype == "HK":
    stockList = getStockHKList(node = 0)
#print(stockList)
sdList = [2]
dayList = [30,60,90,120]
paramList = list(product(sdList, dayList))
data = []
for stock in stockList:
    entry = {
        "stock": {
            "name": stock,
            "region": stocktype,
            "component": component,
            "parameter": []}
        
    }
    #print(entry["stock"])
    for (i,(SD,day)) in enumerate(paramList):
        entry["stock"]["parameter"].append([{"SD": SD}, {"day": day}])
    #print(entry)
    data.append(entry)

with open('info/stock{}Json.json'.format(stocktype), 'w') as fp:
    json.dump(data, fp, indent=4)