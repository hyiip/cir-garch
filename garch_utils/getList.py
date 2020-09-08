import json
import itertools

def getIndexList(mode = 1):
    if mode == "create":
        index = []
        with open('updating/info.csv', 'r') as f:
            for (i,line) in enumerate(f.readlines()):
                if i == 0:
                    continue
                index.append(line.strip().split(",")[0])
    elif mode == 1:
        with open('info/indexJson.json') as f:
            data = json.load(f)
            index = [f["index"]["name"] for f in data]
    return index

def getStockHKList(mode = 1):
    if mode == 0:
        stock = []
        with open('info/stockListHK.txt', 'r') as f:
            for (i,line) in enumerate(f.readlines()):
                stock.append(line.strip())
    elif mode == 1:
        with open('info/stockHKJson.json') as f:
            data = json.load(f)
            stock = [f["stock"]["name"] for f in data]
    return stock

def getStockUSList(mode = 1):
    if mode == 0:
        stock = []
        with open('info/stockListUS.txt', 'r') as f:
            for (i,line) in enumerate(f.readlines()):
                stock.append(line.strip().split(" ")[0])
    elif mode == 1:
        with open('info/stockUSJson.json') as f:
            data = json.load(f)
            stock = [f["stock"]["name"] for f in data]
    return stock

def getStockList(region, mode = 1):
    if mode == 0:
        stock = []
        with open('info/stockList{}.txt'.format(region), 'r') as f:
            for (i,line) in enumerate(f.readlines()):
                stock.append(line.strip())
    elif mode == 1:
        with open('info/stock{}Json.json'.format(region)) as f:
            data = json.load(f)
            stock = [f["stock"]["name"] for f in data]
    return stock

def getItemNameFromJson(itemType,region):
    filename = 'info/{}Json.json'.format(itemType + region)
    with open(filename) as f:
        data = json.load(f)
        item = [f[itemType]["name"] for f in data]
    return item

def getParameterListFromJson(itemType,region,mode = "normal"):
    if mode == "plot":
        filename = 'info/{}Json_plot.json'.format(itemType + region)
    else:
        filename = 'info/{}Json.json'.format(itemType + region)
    with open(filename) as f:
        data = json.load(f)
        itemList = [f[itemType] for f in data]
        if "bondfloat" not in itemType:
            parameter = [(item["name"], para["SD"], para["day"], itemType+region) for item in itemList for para in item["parameter"]]
        else:
            parameter = [(item["name"], para["SD"], para["day"], itemType+region, para["tor"]) for item in itemList for para in item["parameter"]]

    return parameter
def inputForm():
    region = ""
    print("input item type (stock/index/bond)")
    itemType = input().strip()
    if itemType == "stock":
        print("input item region eg.(US/HK)")
        region = input().strip()
    if "bond" in itemType:
        print("input item region eg.(GER)")
        region = input().strip()
    return itemType, region

if __name__ == '__main__':
    itemType, region = inputForm()
    getParameterListFromJson(itemType,region)