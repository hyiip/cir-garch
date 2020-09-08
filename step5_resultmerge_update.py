#merge result after matlab & eviews

import itertools
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

from pathlib import Path
from getIndexList import getIndexList
    

def resultmerge(params):
    SDint = params[0]
    day = params[1]
    mode = params[2]
    index = params[3]
    
    MA = str(day)
    SD = str(int(SDint*100))
    
    #xlsxPath = "all/excel/"
    #Path(xlsxPath).mkdir(parents=True, exist_ok=True)
    
    #xlsxFile = "{}_day{}_SD{}_{}_index.xlsx".format(mode,MA,SD,index)
    #writer = pd.ExcelWriter(xlsxPath + xlsxFile,date_format = 'yyyy/mm/dd',datetime_format='yyyy/mm/dd')
    
    resultNames = "day{}_SD{}_{}.csv".format(MA,SD,index)
    
    #index = names[loc+1:-4]
    #print(names[loc+1:-4])
    
    pathString = "SD{}/day{}/{}/".format(SD,MA,mode)
    
    pathname = "updating/result/" + pathString
    
    path = Path(pathname)
    path.mkdir(parents=True, exist_ok=True)
    
    matlabname = "cir_{}_bounded_day{}_SD{}_{}.csv".format(mode,MA,SD,index)
    matlabPath = "updating/temp/" + pathString
    
    eviewsname = "garch_{}_bounded_day{}_SD{}_{}.csv".format(mode,MA,SD,index)
    eviewsPath = "updating/eviews/" + pathString
    
    tablePath = "updating/table/"+ "SD{}/day{}/".format(SD,MA)
    
    bounded = pd.read_csv(matlabPath + matlabname, parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=[" NaN"])
    #firstString = (list(bounded)[0])
    #if(firstString.find("cir_"))==-1:
    #    bounded = bounded.add_prefix('cir_')
    #bounded.to_csv(matlabPath + matlabname, sep=",", index=True) #rename add prefix to column name
    
    eviews = pd.read_csv(eviewsPath + eviewsname, parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])
    eviews = eviews.add_prefix('garch_')
    eviews.rename(columns={"garch_x"+mode+"_kappa":"garch_kappa","garch_x"+mode+"_kappa_se":"garch_kappa_se","garch_x"+mode+"_sigma":"garch_sigma","garch_x"+mode+"_sigma_se":"garch_sigma_se","garch_x"+mode+"_theta":"garch_theta","garch_x"+mode+"_theta_se":"garch_theta_se"},inplace=True)
    
    
    f = open(tablePath + resultNames)
    table = pd.read_csv(tablePath + resultNames, parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])
    
    #print(table.head(1))
    
    all = pd.concat([table,bounded,eviews], axis=1)
    
    all["cir_kappa_lb"] = all["cir_kappa"] - 1.96 * all["cir_kappa_sd"]
    all["cir_kappa_ub"] = all["cir_kappa"] + 1.96 * all["cir_kappa_sd"]
    all["cir_theta_lb"] = all["cir_theta"] - 1.96 * all["cir_theta_sd"]
    all["cir_theta_ub"] = all["cir_theta"] + 1.96 * all["cir_theta_sd"]
    all["cir_sigma_lb"] = all["cir_sigma"] - 1.96 * all["cir_sigma_sd"]
    all["cir_sigma_ub"] = all["cir_sigma"] + 1.96 * all["cir_sigma_sd"]
    all["garch_kappa_lb"] = all["garch_kappa"] - 1.96 * all["garch_kappa_se"]
    all["garch_kappa_ub"] = all["garch_kappa"] + 1.96 * all["garch_kappa_se"]
    all["garch_kappa_z"] = all["garch_kappa"] / all["garch_kappa_se"]
    all["garch_theta_lb"] = all["garch_theta"] - 1.96 * all["garch_theta_se"]
    all["garch_theta_ub"] = all["garch_theta"] + 1.96 * all["garch_theta_se"]
    all["garch_theta_z"] = all["garch_theta"] / all["garch_theta_se"]
    

    #theta -> sigma
    if all["garch_sigma"].sum()<0:
        sigmaCondition = 0
    else:
        sigmaCondition = 1
        
    if sigmaCondition:
        all["garch_sigma_lb"] = all["garch_sigma"] - 1.96 * all["garch_sigma_se"]
        all["garch_sigma_ub"] = all["garch_sigma"] + 1.96 * all["garch_sigma_se"]
        all["garch_sigma_z"] = all["garch_sigma"] / all["garch_sigma_se"]
    else:
        all["garch_sigma_lb"] = 0
        all["garch_sigma_ub"] = 0
        all["garch_sigma_z"] = 0
        
    all = all[["Close",MA+"MA","Normalize","bounded_x","cir_leakage",
        "cir_kappa","cir_kappa_sd","cir_kappa_lb","cir_kappa_ub","cir_kappa_z",
        "garch_kappa","garch_kappa_se","garch_kappa_lb","garch_kappa_ub","garch_kappa_z",
        "cir_theta","cir_theta_sd","cir_theta_lb","cir_theta_ub","cir_theta_z",
        "garch_theta","garch_theta_se","garch_theta_lb","garch_theta_ub","garch_theta_z",
        "cir_sigma","cir_sigma_sd","cir_sigma_lb","cir_sigma_ub","cir_sigma_z",
        "garch_sigma","garch_sigma_se","garch_sigma_lb","garch_sigma_ub","garch_sigma_z"]]
    
    all.to_csv(pathname + resultNames, sep=",", index=True)
    #all.to_excel(writer,index)
    #writer.save()
    print(pathname + resultNames)
    
def resultMerger():
    sdList = [1.5,1.75,2,2.5]
    dayList = [30,50,60,90,120]
    indexList = getIndexList()
    modeList = ["expand","roll"]
    paramList = list(itertools.product(sdList,dayList,modeList,indexList))
    for param in paramList:
        resultmerge(param)
    return 0
        
if __name__ == '__main__':
    resultMerger()