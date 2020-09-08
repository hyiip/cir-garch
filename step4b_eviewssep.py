#merge result after matlab & eviews

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from getIndexList import getIndexList
import itertools

from pathlib import Path


def eviewssep(params):
    SDint = params[0]
    day = params[1]
    index = params[2]
    
    SD = str(int(SDint*100))
    MA = str(day)
    #SD = 2
    SDstring = "SD" + str(int(SD*100)) + "/"
    #MA = "90"

    originalpath = "day" + MA + "/"
    
    filePath = "updating/eviews/SD{}/day{}/garch/".format(SD,MA)
    
    fileName = "garch_bounded_day{}_SD{}_{}.csv".format(MA,SD,index)
    rollSavenames = "garch_roll_bounded_day{}_SD{}_{}.csv".format(MA,SD,index)
    expandSavenames = "garch_expand_bounded_day{}_SD{}_{}.csv".format(MA,SD,index)
    
    rollname = "updating/eviews/SD{}/day{}/roll/".format(SD,MA)
    rollpath = Path(rollname)
    rollpath.mkdir(parents=True, exist_ok=True)
    expandname = "updating/eviews/SD{}/day{}/expand/".format(SD,MA)
    expandpath = Path(expandname)
    expandpath.mkdir(parents=True, exist_ok=True)
    
    #pathname = "all/" + originalpath + indexname + "/image/"
    #print(pathname)
    #path = Path(pathname)
    #path.mkdir(parents=True, exist_ok=True)
    expandDf = pd.read_csv(filePath + fileName , usecols = [0,1,2,3,4,5,6], parse_dates=['date'] , dayfirst=True, index_col=0 , na_values=["null"])
    rollDf = pd.read_csv(filePath + fileName , usecols = [0,7,8,9,10,11,12], parse_dates=['date'] , dayfirst=True, index_col=0 , na_values=["null"])
    expandDf.index.names = ['Date']
    rollDf.index.names = ['Date']
    
    
    expandDf.to_csv(expandname + expandSavenames, sep=",", index=True)
    rollDf.to_csv(rollname + rollSavenames, sep=",", index=True)
    print(fileName)

def eViewMerge():
    sdList = [1.5,1.75,2,2.5]
    dayList = [30,50,60,90,120]
    indexList = getIndexList()
    paramList = list(itertools.product(sdList,dayList,indexList))
    for param in paramList:
        eviewssep(param)
    return 0
        
if __name__ == '__main__':
    eViewMerge()