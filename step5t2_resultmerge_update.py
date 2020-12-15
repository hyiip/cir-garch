#merge result after matlab & eviews

import itertools
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

from pathlib import Path
from garch_utils.getList import getItemNameFromJson,getParameterListFromJson
from garch_utils.inputForm import inputForm
 

def resultmerge(fullParams):
    params = fullParams[0]
    itemmode = fullParams[1]
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
    
    #xlsxPath = "allData/excel/"
    #Path(xlsxPath).mkdir(parents=True, exist_ok=True)
    
    #xlsxFile = "{}_day{}_SD{}_{}_index.xlsx".format(mode,MA,SD,index)
    #writer = pd.ExcelWriter(xlsxPath + xlsxFile,date_format = 'yyyy/mm/dd',datetime_format='yyyy/mm/dd')
    
    
    #index = names[loc+1:-4]
    #print(names[loc+1:-4])
    
    pathString = "SD{}/day{}/{}/".format(SD,MA,mode)
    #itemmode = itemType.replace("bond","").replace("GER","")
    if itemmode not in ["upper","lower"]:
        itemmode = ""
    else:
        itemmode =  itemmode
    
    if not epsilon == 0:
        resultNames = "{}_tor{}_day{}_SD{}_{}.csv".format(mode,epsilon,MA,SD,item)
        pathname = itemType + "/updating/tor{}/result/".format(epsilon) + pathString
    
        matlabname = "cir_{}_bounded_tor{}_day{}_SD{}_{}.csv".format(mode,epsilon,MA,SD,item)
        matlabPath = itemType + "/updating/tor{}/temp/".format(epsilon) + pathString
        
        tablePath = itemType + "/updating/tor{}/table/".format(epsilon)+ "SD{}/day{}/".format(SD,MA)
    else:
        
        if not itemmode == "":
            resultNames = "{}_{}_day{}_SD{}_{}.csv".format(mode,itemmode,MA,SD,item)
            matlabname = "cir_{}_bounded_{}_day{}_SD{}_{}.csv".format(mode,itemmode,MA,SD,item)
            tableName = "{}_day{}_SD{}_{}.csv".format(itemmode,MA,SD,item)
        else:
            resultNames = "{}_day{}_SD{}_{}.csv".format(mode,MA,SD,item)
            matlabname = "cir_{}_bounded_day{}_SD{}_{}.csv".format(mode,MA,SD,item)
            tableName = "day{}_SD{}_{}.csv".format(MA,SD,item)

        pathname = itemType + "/updating/result/" + pathString
    
        matlabPath = itemType + "/updating/temp/" + pathString
        tablePath = itemType + "/updating/table/"+ "SD{}/day{}/".format(SD,MA)
   
    path = Path(pathname)
    path.mkdir(parents=True, exist_ok=True)
    
    bounded = pd.read_csv(matlabPath + matlabname, parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=[" NaN"])
    #firstString = (list(bounded)[0])
    #if(firstString.find("cir_"))==-1:
    #    bounded = bounded.add_prefix('cir_')
    #bounded.to_csv(matlabPath + matlabname, sep=",", index=True) #rename add prefix to column name
    
    
    table = pd.read_csv(tablePath + tableName, parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])
    if (not "bond" in itemType) or (not "GER" in itemType) :
        allData = pd.concat([table,bounded], axis=1)
    #print(table.head(1))
    else:
        bank = pd.read_csv(itemType +"/updating/bank.csv", parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])
        bank = bank.drop(bank.index[0:day-1])
        bank = bank[0:len(table.index)]
        allData = pd.concat([table,bounded,bank], axis=1)

    allData["cir_kappa_lb"] = allData["cir_kappa"] - 1.96 * allData["cir_kappa_sd"]
    allData["cir_kappa_ub"] = allData["cir_kappa"] + 1.96 * allData["cir_kappa_sd"]
    allData["cir_theta_lb"] = allData["cir_theta"] - 1.96 * allData["cir_theta_sd"]
    allData["cir_theta_ub"] = allData["cir_theta"] + 1.96 * allData["cir_theta_sd"]
    allData["cir_sigma_lb"] = allData["cir_sigma"] - 1.96 * allData["cir_sigma_sd"]
    allData["cir_sigma_ub"] = allData["cir_sigma"] + 1.96 * allData["cir_sigma_sd"]
    ''' allData = allData[[allData.columns[0],MA+"MA","Normalize", 'S_U', 'S_L',"thickness","bounded_x","cir_leakage",
        "cir_kappa","cir_kappa_sd","cir_kappa_lb","cir_kappa_ub","cir_kappa_z",
        "cir_theta","cir_theta_sd","cir_theta_lb","cir_theta_ub","cir_theta_z",
        "cir_sigma","cir_sigma_sd","cir_sigma_lb","cir_sigma_ub","cir_sigma_z"]]
    '''
    if itemmode not in ["upper","lower"]:
        if ("bond" not in itemType):
            allData = allData[[allData.columns[0],MA+"MA","Normalize", 'S_U', 'S_L', "bounded_x","cir_leakage",
                "cir_kappa","cir_kappa_sd","cir_kappa_lb","cir_kappa_ub","cir_kappa_z",
                "cir_theta","cir_theta_sd","cir_theta_lb","cir_theta_ub","cir_theta_z",
                "cir_sigma","cir_sigma_sd","cir_sigma_lb","cir_sigma_ub","cir_sigma_z"]]

            #allData.rename(columns={'bounded_x': 'x'}, inplace=True)
            allData.columns = [allData.columns[0],MA+"MA","S/S_A", 'S_U', 'S_L', "s","Leakage Ratio",
            "kappa","kappa_SE","kappa_lb","kappa_ub","kappa_z",
            "theta","theta_SE","theta_lb","theta_ub","theta_z",
            "sigma","sigma_SE","sigma_lb","sigma_ub","sigma_z"]
        else:
            allData = allData[[allData.columns[0],MA+"MA","Bank","Normalize", 'S_U', 'S_L', "thickness", "bounded_x","cir_leakage",
                "cir_kappa","cir_kappa_sd","cir_kappa_lb","cir_kappa_ub","cir_kappa_z",
                "cir_theta","cir_theta_sd","cir_theta_lb","cir_theta_ub","cir_theta_z",
                "cir_sigma","cir_sigma_sd","cir_sigma_lb","cir_sigma_ub","cir_sigma_z"]]

            #allData.rename(columns={'bounded_x': 'x'}, inplace=True)
            allData.columns = [allData.columns[0],MA+"MA","Bank's Rate","S/S_A", 'S_U', 'S_L', 'Band Width', "s","Leakage Ratio",
            "kappa","kappa_SE","kappa_lb","kappa_ub","kappa_z",
            "theta","theta_SE","theta_lb","theta_ub","theta_z",
            "sigma","sigma_SE","sigma_lb","sigma_ub","sigma_z"]


    else:
        if ("GER" not in itemType):
            allData = allData[[allData.columns[0],MA+"MA","Normalize", 'S_U', 'S_L', "bounded_x","cir_leakage",
                "cir_kappa","cir_kappa_sd","cir_kappa_lb","cir_kappa_ub","cir_kappa_z",
                "cir_theta","cir_theta_sd","cir_theta_lb","cir_theta_ub","cir_theta_z",
                "cir_sigma","cir_sigma_sd","cir_sigma_lb","cir_sigma_ub","cir_sigma_z"]]

            #allData.rename(columns={'bounded_x': 'x'}, inplace=True)
            allData.columns = [allData.columns[0],MA+"MA","S/S_A", 'S_U', 'S_L', "s","Leakage Ratio",
            "kappa","kappa_SE","kappa_lb","kappa_ub","kappa_z",
            "theta","theta_SE","theta_lb","theta_ub","theta_z",
            "sigma","sigma_SE","sigma_lb","sigma_ub","sigma_z"]
        else:
            allData = allData[[allData.columns[0],MA+"MA","Bank","Normalize", 'S_U', 'S_L', "bounded_x","cir_leakage",
                "cir_kappa","cir_kappa_sd","cir_kappa_lb","cir_kappa_ub","cir_kappa_z",
                "cir_theta","cir_theta_sd","cir_theta_lb","cir_theta_ub","cir_theta_z",
                "cir_sigma","cir_sigma_sd","cir_sigma_lb","cir_sigma_ub","cir_sigma_z"]]

            #allData.rename(columns={'bounded_x': 'x'}, inplace=True)
            allData.columns = [allData.columns[0],MA+"MA","Bank's Rate","S/S_A", 'S_U', 'S_L', "s","Leakage Ratio",
            "kappa","kappa_SE","kappa_lb","kappa_ub","kappa_z",
            "theta","theta_SE","theta_lb","theta_ub","theta_z",
            "sigma","sigma_SE","sigma_lb","sigma_ub","sigma_z"]
    allData.to_csv(pathname + resultNames, sep=",", index=True)
    #allData.to_excel(writer,index)
    #writer.save()
    print(pathname + resultNames)
    
def resultMerger(itemType , region, mode="hybrid"):
    tempList = getParameterListFromJson(itemType,region)
    modeList = ["roll"]
    paramList = [((a,*b),mode) for a,b in itertools.product(modeList,tempList)]
    for param in paramList:
        resultmerge(param)
    return 0
        
if __name__ == '__main__':
    #itemType, region = inputForm()
    #resultMerger(itemType , region)
    for mode in ["lower"]:
        itemType = "bond{}".format(mode)
        region = "FR"
        resultMerger(itemType,region, mode = mode)