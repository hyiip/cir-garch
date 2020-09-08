import json
from garch_utils.getList import getStockList #pylint: disable=import-error

with open('info/stockHKJson.json') as f:
  data = json.load(f)


for item in data:
    print(item["stock"])

itemlist = [f["stock"]["name"] for f in data]
print(itemlist)
print("-------")
print(getStockList("US"))
# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
#print(data)