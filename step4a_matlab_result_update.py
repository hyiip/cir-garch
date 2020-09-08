#merge result after matlab & eviews

import pandas as pd
import os.path
import numpy as np
from os import listdir
from os.path import isfile, join

from pathlib import Path

import itertools
from garch_utils.getList import getItemNameFromJson,getParameterListFromJson
from garch_utils.inputForm import inputForm

def matlabUpdate(params):
    mode = params[0]
    item = params[1]
    SDint = params[2]
    day = params[3]
    itemType = params[4]
    try:
        epsilon = float(params[5])
    except:
        epsilon = 0
    
    MA = str(day)
    SD = str(int(SDint*100))
    itemmode = itemType.replace("bond","").replace("GER","")
    if itemmode not in ["upper","lower"]:
        itemmode = ""
    else:
        itemmode =  itemmode
    #MApath = "day" + MA + "/"
    if not epsilon == 0:
        filenames = "cir_{}_bounded_tor{}_day{}_SD{}_{}.csv".format(mode,epsilon,MA,SD,item)
        
        originalPath = "{}/original/tor{}/temp/SD{}/day{}/{}/".format(itemType,epsilon,SD,MA,mode)
        updatePath = "{}/updating/tor{}/temp/new/SD{}/day{}/{}/".format(itemType,epsilon,SD,MA,mode)
        newPath = "{}/updating/tor{}/temp/SD{}/day{}/{}/".format(itemType,epsilon,SD,MA,mode)
    
    else:
        if not itemmode == "":
            filenames = "cir_{mode}_bounded_{itemmode}_day{MA}_SD{SD}_{item}.csv".format(mode = mode,itemmode = itemmode,MA = MA,SD = SD,item = item)
        else:
            filenames = "cir_{mode}_bounded_day{MA}_SD{SD}_{item}.csv".format(mode = mode,MA = MA,SD = SD,item = item)

        originalPath = "{}/original/temp/SD{}/day{}/{}/".format(itemType,SD,MA,mode)
        updatePath = "{}/updating/temp/new/SD{}/day{}/{}/".format(itemType,SD,MA,mode)
        newPath = "{}/updating/temp/SD{}/day{}/{}/".format(itemType,SD,MA,mode)
    
    #writer = pd.ExcelWriter(mode + "_" + MA + "days_SD" + SD +"_index.xlsx",date_format = 'yyyy/mm/dd',datetime_format='yyyy/mm/dd')
    path = Path(newPath)
    path.mkdir(parents=True, exist_ok=True)
    
    #index = names[loc+1:-4]
    #print(names[loc+1:-4])
    
    
    #pathname = "updating/result/SD{}/{}/day{}/".format(SD,mode,MA)
    
    #path = Path(pathname)
    #path.mkdir(parents=True, exist_ok=True)
    
    update = pd.read_csv(updatePath + filenames, parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])

    if os.path.isfile(originalPath + filenames):
        raw = pd.read_csv(originalPath + filenames, parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])
        new = pd.concat([raw,update])
        new = new[~new.index.duplicated(keep='last')]
    else:
        new = update
    new.to_csv(newPath + filenames, sep=",", index=True)
    print(newPath + filenames)
    

    
def matlabUpdateMain(itemType , region,mode="hybrid"):
    tempList = getParameterListFromJson(itemType,region)
    #modeList = ["expand","roll"]
    modeList = ["roll","expand"]
    paramList = [(a,*b) for a,b in itertools.product(modeList,tempList)]
    for param in paramList:
        matlabUpdate(param)
    return 0
    
if __name__ == '__main__':
    #itemType, region = inputForm()
    for mode in ["default"]:
        itemType = "vixir"
        region = ""
        matlabUpdateMain(itemType,region, mode = mode)