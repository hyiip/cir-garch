import pyeviews as evp
from pathlib import Path
import pandas as pd
import numpy as np
import itertools
import multiprocessing
import time
#from getIndexList import getIndexList

def eviewsRun(params):
    
    eviewsapp = evp.GetEViewsApp(instance='new', showwindow=True) #showwindow=True, otherwise never know what have happened
    info = pd.read_csv("updating/info.csv",index_col=0)
    SD = params[0]
    day = params[1]
    index = params[2]
    offset = int(info.loc[index]["offset"]-1)
    #offset = -1
    mypath = str(Path().absolute())
    command = "run \"eviewsbatch_dropna.prg\" {} {} \"{}\" {}".format(SD,day,index,offset)
    evp.Run("cd " + mypath, app=eviewsapp)
    evp.Run(command, app=eviewsapp)
    print(command)
    eviewsapp.Hide()
    eviewsapp = None
    evp.Cleanup()


def eviewsbatch():
    start = time.time()
    sdList = [1.5,1.75,2,2.5]
    dayList = [30,50,60,90,120]
    indexList = getIndexList()
    paramlist = list(itertools.product(sdList,dayList,indexList))

    paramlist = paramlist

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
    eviewsbatch()