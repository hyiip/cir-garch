#to transform index to ln bounded form

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from pathlib import Path
from garch_utils.getList import getItemNameFromJson,getParameterListFromJson
import itertools
import warnings
from garch_utils.inputForm import inputForm
import logging

def extractRaw(itemList,itemType):
    filepath = {
        "removed": "{}/updating/raw/".format(itemType),
        "extracted": "{}/updating/extracted/".format(itemType),
        "raw": "{}/original/raw/".format(itemType),
        "new": "{}/updating/new/".format(itemType)
        }
    for f in filepath.values():
        tempPath = Path(f)
        tempPath.mkdir(parents=True, exist_ok=True)
    for item in itemList:
        #rawName = item + "_temp.csv"
        #indexCSV = item + ".csv"
        new = pd.read_csv("{}{}_temp.csv".format(filepath["new"],item), parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])
        new = new.dropna() #remove null values
        raw = pd.read_csv("{}{}.csv".format(filepath["raw"],item), parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])
        result = pd.concat([raw,new])
        result = result[~result.index.duplicated(keep='last')]
        if "vixir" in itemType:
            result = result.drop(columns = ["Volume"])
            result = result.apply(lambda x: 1/x)
        if "exchange" in itemType:
            result = result.drop(columns = ["Change %"])
            if item == "USDHKD":
                result[result >= 7.85] = 7.85-1e-6
                result[result <= 7.75] = 7.75+1e-6
        result.to_csv(filepath["removed"] + item + ".csv", sep=",", index=True)
        result["Close"].to_csv(filepath["extracted"] + item + ".csv", sep=",", index=True, header=True)

def setUSDHKD(itemType):
    filepath = {
        "removed": "{}/updating/raw/".format(itemType),
        "extracted": "{}/updating/extracted/".format(itemType),
        "raw": "{}/original/raw/".format(itemType),
        "new": "{}/updating/new/".format(itemType)
        }
    for f in filepath.values():
        tempPath = Path(f)
        tempPath.mkdir(parents=True, exist_ok=True)
    input_item = "USDHKD"
    output_item = "HKDUSD"
    result = pd.read_csv(filepath["removed"] + input_item + ".csv", parse_dates=['Date'] , dayfirst=True, index_col=0 , na_values=["null"])
    result = result.apply(lambda x: 1/x)
    result.to_csv(filepath["removed"] + output_item + ".csv", sep=",", index=True)
    result["Close"].to_csv(filepath["extracted"] + output_item + ".csv", sep=",", index=True, header=True)
    print("USDHKD set")

def processRaw(params,itemType, mode = "curr"):
    print(mode)
    item = params[0]
    SD = params[1]
    day = params[2]
    print(params)
    try:
        epsilon = float(params[4])
    except:
        epsilon = 0
    averagedate = day
    MAname = "{}MA".format(day)
    SDstring = int(SD*100)
    filestring = "tor{}_day{}_SD{}_".format(epsilon,day,SDstring)
    
    names = item + ".csv"
    if not epsilon == 0:
        filepath = {
            "extracted": "{}/updating/extracted/".format(itemType),
            "toanalysis": "{}/updating/tol{}/toanalysis/SD{}/day{}/".format(itemType,epsilon,SDstring,day),
            "table": "{}/updating/tol{}/table/SD{}/day{}/".format(itemType,epsilon,SDstring,day),
            "root": "{}/updating/tol{}/".format(itemType,epsilon),
            
            }
        if  mode in ["lower", "upper"]:
            filestring = "{}_tol{}_day{}_SD{}_".format(mode,epsilon,day,SDstring)
        else:
            filestring = "tol{}_day{}_SD{}_".format(epsilon,day,SDstring)
    else:
        filepath = {
            "extracted": "{}/updating/extracted/".format(itemType),
            "toanalysis": "{}/updating/toanalysis/SD{}/day{}/".format(itemType,SDstring,day),
            "table": "{}/updating/table/SD{}/day{}/".format(itemType,SDstring,day),
            "root": "{}/updating/".format(itemType),
            }
        if mode in ["lower", "upper"]:
            filestring = "{}_day{}_SD{}_".format(mode,day,SDstring)
        else:
            filestring = "day{}_SD{}_".format(day,SDstring)
    for f in filepath.values():
        tempPath = Path(f)
        tempPath.mkdir(parents=True, exist_ok=True)

    Si = pd.read_csv("{}{}.csv".format(filepath["extracted"],item), parse_dates=['Date'] , dayfirst=True,  usecols=[0,1], index_col=0 , na_values=["null"])

    Si = Si.dropna() #remove null values

    Sm = Si.rolling(window=averagedate).mean() #rolling mean of <averagedate> data
    Sm = Sm.dropna()
    Sm.columns = [MAname]
    Si = Si.drop(Si.index[0:averagedate-1]) #match two index#

    normalize = Si.div(Sm[MAname], axis='index') 
    normalize.columns = ["Normalize"]
    #warnings.simplefilter("error")
    #SU = (1+0.25*SD) * Sm[MAname]
    #SL = (1-0.25*SD) * Sm[MAname]
    logging.basicConfig(level=logging.DEBUG, filename=filepath["root"] + "errorlog.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    #epsilon = 0.4

    if mode == "exchange":
        if item == "HKDUSD":
            mode = "lowerCurr"
        elif item == "USDHKD":
            mode = "upperCurr"

    if mode == "hybrid":
        SU = pd.Series(Sm[MAname]*(1+0.25*SD), name = "S_U")
        SL = pd.Series(Sm[MAname]*(1-0.25*SD), name = "S_L")
        thickness = pd.Series(Sm[MAname]*(1-0.25*SD), name = "thickness").copy()

        wide = 0
        for i in range(0,len(Sm[MAname])):
            if abs(Sm[MAname][i]) >= epsilon:
                wide = 0.25 * SD * Sm[MAname][i]
            
            SU[i] = Sm[MAname][i] + abs(wide) 
            SL[i] = Sm[MAname][i] - abs(wide)
            thickness[i] = abs(wide) 
        testSeries = ( (SU - Si.iloc[:,0]) / (SU - SL) ) 
    elif mode == "hybrid2":
        SU = pd.Series(Sm[MAname]*(1+0.25*SD), name = "S_U")
        SL = pd.Series(Sm[MAname]*(1-0.25*SD), name = "S_L")
        thickness = pd.Series(Sm[MAname]*(1-0.25*SD), name = "thickness").copy()

        wide = 0
        for i in range(0,len(Sm[MAname])):
            if abs(Sm[MAname][i]) >= epsilon:
                wide = 0.25 * SD * Sm[MAname][i]
            else:
                wide = 0.25 * SD * epsilon
            SU[i] = Sm[MAname][i] + abs(wide) 
            SL[i] = Sm[MAname][i] - abs(wide)
            thickness[i] = abs(wide) 
        testSeries = ( (SU - Si.iloc[:,0]) / (SU - SL) ) 

    elif mode == "fixed":
        SU = pd.Series(Sm[MAname]*0+0.5, name = "S_U")
        SL = pd.Series(Sm[MAname]*0-0.5, name = "S_L")
        if item == "F91010Y_mod":
            testSeries = np.exp(-Si.iloc[:,0])
        else:
            testSeries = ( (SU - Si.iloc[:,0]) / (SU - SL) ) 
    elif mode == "lower":
        SU = pd.Series(Sm[MAname]*(1+0.25*SD), name = "S_U")
        SL = pd.Series(Sm[MAname]*0, name = "S_L")
        if item == "F91010Y_mod":
            testSeries = np.exp(-Si.iloc[:,0])
        else:
            testSeries = ( (SU - Si.iloc[:,0]) / (SU - SL) ) 
    elif mode == "upper":
        SU = pd.Series(Sm[MAname]*(1+0.25*SD), name = "S_U")
        SL = pd.Series(Sm[MAname]*0, name = "S_L")
        testSeries = ( (Si.iloc[:,0] - SL) / (SU - SL) ) 
    elif mode == "lowerCurr":
        SU = pd.Series(Sm[MAname]*0 + 1/7.75, name = "S_U")
        SL = pd.Series(Sm[MAname]*0 + 1/7.85, name = "S_L")
        testSeries = ( (SU - Si.iloc[:,0]) / (SU - SL) ) 
    elif mode == "upperCurr":
        SU = pd.Series(Sm[MAname]*0 + 7.85, name = "S_U")
        SL = pd.Series(Sm[MAname]*0 + 7.75, name = "S_L")
        testSeries = ( (Si.iloc[:,0] - SL) / (SU - SL) ) 
    elif mode == "vix":
        SU = pd.Series(Sm[MAname]*(1+0.25*SD), name = "S_U")
        SL = pd.Series(Sm[MAname]*(1-0.25*SD), name = "S_L")
        testSeries = ( (Si.iloc[:,0] - SL) / (SU - SL) ) 
    elif mode == "vixir":
        SU = pd.Series(Sm[MAname]*(1+0.25*SD), name = "S_U")
        SL = pd.Series(Sm[MAname]*(1-0.25*SD), name = "S_L")
        testSeries = ( (SU - Si.iloc[:,0]) / (SU - SL) ) 
    else:
        SU = pd.Series(Sm[MAname]*(1+0.25*SD), name = "S_U")
        SL = pd.Series(Sm[MAname]*(1-0.25*SD), name = "S_L")
        testSeries = ( (SU - Si.iloc[:,0]) / (SU - SL) ) 
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        transformed = pd.DataFrame(-np.log(testSeries) )
        if any(transformed[0]<0):
            warnings.warn("negative x")
    if len(w) != 0:
        print(w[0])
        print(w[0].message)
        logging.warning("{} - ".format(params) +f'{w[0].category.__name__}: {str(w[0].message)}')
    #transformed.columns = ["bounded_x"]
    
    #SU = Sm[MAname].apply(lambda x: (1+0.25*SD) * x if (1+0.25*SD) * abs(x)>=epsilon else epsilon)
    #SL = Sm[MAname].apply(lambda x: (1-0.25*SD) * x if (1+0.25*SD) * abs(x)>=epsilon else -epsilon)

    transformed.columns = ["bounded_x"]
    #transformed_raw.columns = ["bounded_x_raw"]

    table = pd.concat([Si, Sm, normalize,SU,SL,transformed], axis=1)
    colname = list(table.columns)
    colname[3] = "S_U"
    colname[4] = "S_L"
    table.columns = colname
    #table.rename(columns={ table.columns[4]: "S_U" }, inplace = True)
    transformed.to_csv(filepath["toanalysis"] + "bounded_" + filestring + names, sep=",", index=True)
    table.to_csv(filepath["table"] + filestring + names, sep=",", index=True)
    
        
        
def updateRaw(itemType,region,mode):
    #sdList = [1.5,1.75,2,2.5]
    #dayList = [30,50,60,90,120]
    indexList = getItemNameFromJson(itemType,region)
    
    if "bond" not in itemType:
        extractRaw(indexList,itemType + region)
        print("extractRaw done")
    if "USDHKD" in indexList:
        setUSDHKD(itemType + region)
    paramList = getParameterListFromJson(itemType,region)
    #paramList = (("0175.HK",2,30,"stockHK"),("0175.HK",2,60,"stockHK"),("0175.HK",2,90,"stockHK"),("0175.HK",2,120,"stockHK"))
    #print(paramList)
    for param in paramList:
        processRaw(param,itemType + region,mode)

    print("processRaw done")
    return 0
    

if __name__ == '__main__':
    #itemType, region = inputForm()
    #updateRaw(itemType,region)
    for mode in ["default"]:
        itemType = "stock"
        region = "HK"
        updateRaw(itemType,region, mode = mode)

