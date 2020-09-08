from itertools import product
import json
import os

def addEntry(itemType,itemList,sdList,dayList,paramList,region = ""):
    #itemType = itemType + region
    filename = 'info/{}Json.json'.format(itemType + region)
    if os.path.exists(filename):
        with open(filename) as f:
            data = json.load(f)
            oldList = [f[itemType]["name"] for f in data]
    else:
        data = []
        oldList = []

    for item in itemList:
        locArray = [i for i, j in enumerate(oldList) if j == item]
        extendList = [{"SD": SD, "day": day} for SD, day in paramList]
        #print(extendList)
        
        if locArray:
            loc = locArray[0]
            oldParm = data[loc][itemType]["parameter"]

            data[loc][itemType]["parameter"].extend([x for x in extendList if x not in oldParm])
        else:
            entry = {
                itemType: {
                    "name": item,
                    "parameter": extendList}
            }
            if itemType == "stock":
                print("{} is a new stock, please input component name (eg HSI)".format(item))
                component = input().strip()
                entry[itemType]["region"] = region
                entry[itemType]["component"] = component
            if itemType == "bond":
                entry[itemType]["region"] = region
            data.append(entry)

    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4)


if __name__ == '__main__':
    region = ""
    print("input type (index/stock/bond)")
    itemType = input().strip()

    if itemType in ("stock", "bond"):
        print("input region")
        region = input().strip()

    print("input item (eg. HSI IXIC) or (eg. 0001.HK 0002.HK)")
    itemList = [f for f in input().split()]

    print("input SD (eg. 2 2.5)")
    sdList = [int(f) if float(f)%1==0 else float(f) for f in input().split()]
    print("input day (eg. 60 90 120)")
    dayList = [int(f) if float(f)%1==0 else float(f) for f in input().split()]
    paramList = list(product(sdList, dayList))
    addEntry(itemType,itemList,sdList,dayList,paramList,region)