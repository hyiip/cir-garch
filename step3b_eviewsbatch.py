import pyeviews as evp
from pathlib import Path
import pandas as pd
import numpy as np
import itertools
import multiprocessing
import time
#from getIndexList import getIndexList

def eviewsRun(fullParams):
    
    eviewsapp = evp.GetEViewsApp(instance='new', showwindow=True) #showwindow=True, otherwise never know what have happened
    info = pd.read_csv("updating/info.csv",index_col=0)
    rollexpand = fullParams[0]
    params = fullParams[1]
    item = params[0]
    SD = params[1]
    day = params[2]
    itemType = params[3]
    offset = int(info.loc[index]["offset"]-1)
    #offset = -1
    mypath = str(Path().absolute())
    command = "run \"eviewsbatch_dropna.prg\" {SD} {day} \"{item}\" {offset} \"{itemType}\" \"{rollexpand}\"".format(
        SD = SD, day = day, item = item, 
        offset = offset, itemType = itemType, 
        rollexpand = rollexpand)
    evp.Run("cd " + mypath, app=eviewsapp)
    evp.Run(command, app=eviewsapp)
    print(command)
    eviewsapp.Hide()
    eviewsapp = None
    evp.Cleanup()


def eviewsbatch(itemType,region,mode="hybrid"):
    start = time.time()
    # sdList = [1.5,1.75,2,2.5]
    # dayList = [30,50,60,90,120]
    # indexList = getIndexList()
    # paramlist = list(itertools.product(sdList,dayList,indexList))

    tempList = getParameterListFromJson(itemType,region)
    modeList = ["roll"]
    paramList = [(a,b) for a,b in itertools.product(modeList,tempList)]
    
    #paramlist = paramlist

    cpuCount = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=1)
    pool.map(eviewsRun,paramlist)
    
    #for param in paramlist:
    #    eviewsRun(param)
    
    end = time.time()
    elapsed = end - start
    print("time used: " + str(elapsed))
    return 0
    
    
if __name__ == '__main__':
    for mode in ["default"]:
        itemType = "vixir_sb"
        region = ""
        eviewsbatch(itemType,region, mode = mode)