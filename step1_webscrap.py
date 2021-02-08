import datetime as dt
from time import mktime
import pandas as pd
import numpy as np
import requests
from os import listdir
from os.path import isfile, join, exists
from pathlib import Path
import re
import sys
import os
from garch_utils.getList import getItemNameFromJson

#def initialzeData(itemType, itemList):

def getDate(itemName,itemType,newFlag):
    now_datetime = dt.datetime.now()
    GMT8tradingday_datetime = dt.datetime.now() - dt.timedelta(days=1)
    now_unixtime = int(mktime(GMT8tradingday_datetime.replace(hour=0,minute=0,second=0,microsecond=0).timetuple()))
    #print("You are extracting data refer to : ", GMT8tradingday_datetime.replace(hour=8,minute=0,second=0,microsecond=0))
    if newFlag:
        latest_unixtime = 0
    else:
        oldraw = pd.read_csv("{}/original/raw/{}.csv".format(itemType,itemName) , index_col=0, na_values=["null"])
        latestdate = oldraw.index[-1]
        latest_unixtime = int(mktime(dt.datetime.strptime(latestdate, "%Y-%m-%d").timetuple()))
    start_date = str(latest_unixtime) # start date timestamp
    end_date   = str(now_unixtime) # end date timestamp
    return start_date, end_date

def getCSV(itemName,itemType,start_date,end_date,newFlag):
    symbol = ""
    print(itemName)
    if itemType == "index":
        symbol = "^" + itemName
    elif "stock" in itemType:
        symbol = itemName
    elif itemType == "curr":
        symbol = itemName + "=X"
    elif itemType == "vix":
        symbol = "^" + itemName
    else:
        symbol = itemName
    crumble_link = 'https://finance.yahoo.com/quote/{0}/history?p={0}'
    crumble_regex = r'CrumbStore":{"crumb":"(.*?)"}'
    cookie_regex = r'set-cookie: (.*?);'
    #quote_link = 'https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb={}'

    link = crumble_link.format(symbol)
    print(link)
    pathname = "{}/updating/new/".format(itemType)
    path = Path(pathname)
    path.mkdir(parents=True, exist_ok=True)
    
    counter = False
    maxTrial = 10
    for i in range(1,maxTrial+1):
        session = requests.Session()
        response = session.get(link)

        # get crumbs

        text = str(response.content)
        match = re.search(crumble_regex, text)
        crumbs = match.group(1)
        
        
        # get cookie

        cookie = session.cookies.get_dict()

        url = "https://query1.finance.yahoo.com/v7/finance/download/%s?period1=%s&period2=%s&interval=1d&events=history&crumb=%s" % (symbol, start_date, end_date, crumbs)
        
        r = requests.get(url,cookies=session.cookies.get_dict(),timeout=i, stream=True)

        out = r.text
        print(out.split("\n")[0])
        if out.split("\n")[0] == "Date,Open,High,Low,Close,Adj Close,Volume":
            counter = True
            break
        print(itemName + " update failed,retrying......")
        if i == maxTrial:
            print("update failed")
            

    oldraw = pd.read_csv("{}/original/raw/{}.csv".format(itemType,itemName) , index_col=0, na_values=["null"])
    latestDate = ""
    if not newFlag:
        latestDate = oldraw.index[-1]
    if counter:
        with open("temp.tmp",'w') as f:
            f.write(out)
        filename = pathname + '{}_temp.csv'.format(itemName)
        data = pd.read_csv("temp.tmp", index_col=0, na_values=["null"])
        os.remove("temp.tmp")
        data = data.dropna()
        firstDate = data.index[0] #drop mismatch
        if newFlag:
            latestDate = firstDate
        print(latestDate, firstDate, latestDate == firstDate)
        if not (latestDate == firstDate):
            data.drop(data.index[:1], inplace=True)
        data.to_csv(filename, sep=",", index=True)
        length = len(data.index)
        if newFlag:
            length = -1
        #return {"Lastest":latestDate, "offset" : length}
    else:
        length = -2 # -1 is reserved
    return latestDate,length
        
        
    
def webScrap(setting,region):
    # start_date = start date timestamp
    # end_date = end date timestamp
    itemList = getItemNameFromJson(setting,region)
    itemType = setting + region
    lengthList = []
    latedateList = []
    filepath = {"info": "{}/updating/".format(itemType), "raw": "{}/original/raw/".format(itemType),"exists": "{}/original/extracted/".format(itemType)}
    infoCSV = "{}{}info.csv".format(filepath["info"],itemType)
    if not os.path.exists(filepath["info"]): #for unknown reason, multiprocess does not support exist_ok = True
        Path(filepath["info"]).mkdir(parents=True, exist_ok=True)
    #infoCSV = "{}/updating/{}info.csv".format(setting,setting)
    if not os.path.exists(infoCSV):
        with open(infoCSV,"w") as f:
            f.write("{},Lastest,offset\n".format(itemType))
    info = pd.read_csv(infoCSV,index_col=0)
    #infoList = list(info.index.values)
    for item in itemList:
        rawname = "{}{}.csv".format(filepath["raw"],item)
        if not os.path.exists(filepath["raw"] + "{}.csv".format(item)):
            if not os.path.exists(filepath["raw"]):
                Path(filepath["raw"]).mkdir(parents=True, exist_ok=True)
            if not os.path.exists(rawname):
                with open(rawname,"w") as f:
                    f.write("Date,Open,High,Low,Close,Adj Close,Volume\n")
        if sum(1 for line in open(rawname)) == 1: 
            newFlag = 1
        else:
            newFlag = 0
        #print(newFlag)
        start_date, end_date = getDate(item,itemType,newFlag)
        #print(start_date, end_date)
        #old method: create a dict afterward
        #new method: update info row by row
        
        #tempDF = pd.DataFrame(getCSV)itemTypeV(item,start_date, end_date)
        latestDate,length  = getCSV(item,itemType,start_date, end_date,newFlag)
        if length == -2:
            continue
        tempdict = {itemType:[item], "Lastest":[latestDate], "offset" : [length]}
        tempdf = pd.DataFrame(tempdict).set_index(itemType)
        if newFlag:
            info = info.append(tempdf)
        info.update(tempdf)
        info = info[~info.index.duplicated(keep='last')]
    #info = {"Index":itemList, "Lastest":latedateList, "offset" : lengthList}
    #df = pd.DataFrame(info).set_index('Index')
    print(info)
    info.to_csv(infoCSV, sep=",", index=True)

    return 0
    
if __name__ == '__main__':
    region = ""
    print("input item type (stock/index)")
    itemType = input().strip()
    if itemType == "stock":
        print("input item region (US/HK)")
        region = input().strip()
    webScrap(itemType,region)