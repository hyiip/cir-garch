import matlab.engine

import itertools
import multiprocessing
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from pathlib import Path
from garch_utils.getList import getItemNameFromJson,getParameterListFromJson
from garch_utils.inputForm import inputForm
import time

def matlabRun(fullParams):
    params = fullParams[0]
    mode = fullParams[1]
    rollexpand = params[0]
    item = params[1]
    SD = params[2]
    day = params[3]
    itemType = params[4]
    try:
        epsilon = str(float(params[5]))
    except:
        epsilon = 0
    
    info = pd.read_csv("{}/updating/{}info.csv".format(itemType,itemType),   index_col=0)
    offset = int(info.loc[item]["offset"]-1) #so for some reason matlab does not support numpy.int64, have to change it to python.int64
    #print( int(info.loc[item]["offset"]-1))
    #offset = -1
    #1/0
    #print(item, SD, day, offset)
    #mode = itemType.replace("bond","").replace("GER","")
    if mode not in ["upper","lower"]:
        mode = ""
    else:
        mode = mode + "_"
    inp = (rollexpand,SD,day,offset,item,itemType,mode)
    print(inp)
    eng = matlab.engine.start_matlab()
    
    if not epsilon == 0:
        eng.CIR_MLE(SD,day,offset,item,itemType,epsilon)
    else:
        eng.CIR_MLE2(rollexpand,SD,day,offset,item,itemType,mode)
    eng.quit()

def matlabBatch(itemType,region,mode="hybrid"):
    start = time.time()
    #sdList = [1.5,1.75,2,2.5]
    #dayList = [30,50,60,90,120]
    #indexList = getItemNameFromJson(itemType,region)
    tempList = getParameterListFromJson(itemType,region)
    modeList = ["roll"]
    paramList = [((a,*b),mode) for a,b in itertools.product(modeList,tempList)]
    #withTypeList = [(n,s,d,itemType + region) for n, s, d in paramList]
    #paramList = (("2319.HK",2,30,"stockHK"),("2319.HK",2,60,"stockHK"))
    cpuCount = multiprocessing.cpu_count()
    #print(cpuCount)
    pool = multiprocessing.Pool(processes=cpuCount)
    pool.map(matlabRun,paramList)
    #for params in paramList:
    #    matlabRun(params)
    end = time.time()
    elapsed = end - start
    print("time used: " + str(elapsed))
    return 0
    
if __name__ == '__main__':
    #itemType, region = inputForm()
    #matlabBatch(itemType , region)
    for mode in ["lower"]:
        itemType = "bond{}".format(mode)
        region = "GER"
        matlabBatch(itemType,region, mode = mode)