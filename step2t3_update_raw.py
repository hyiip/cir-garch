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
        result.to_csv(filepath["removed"] + item + ".csv", sep=",", index=True)
        result["Close"].to_csv(filepath["extracted"] + item + ".csv", sep=",", index=True, header=True)


def processRaw(params,itemType):
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

    filepath = {
        "extracted": "{}/updating/extracted/".format(itemType),
        "toanalysis": "{}/updating/tor{}/toanalysis/SD{}/day{}/".format(itemType,epsilon,SDstring,day),
        "table": "{}/updating/tor{}/table/SD{}/day{}/".format(itemType,epsilon,SDstring,day),
        "root": "{}/updating/tor{}/".format(itemType,epsilon),
        }
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
    warnings.simplefilter("error")
    #SU = (1+0.25*SD) * Sm[MAname]
    #SL = (1-0.25*SD) * Sm[MAname]

    #epsilon = 0.4
    SU = pd.Series(Sm[MAname]*(1+0.25*SD), name = "S_U")
    SL = pd.Series(Sm[MAname]*(1-0.25*SD), name = "S_L")
    thickness = pd.Series(Sm[MAname]*(1-0.25*SD), name = "thickness").copy()

    wide = 0
    for i in range(0,len(Sm[MAname])):
        if abs(Sm[MAname][i]) >= epsilon:
            wide = 0.25*SD * Sm[MAname][i]
        
        SU[i] = Sm[MAname][i] + abs(wide) 
        SL[i] = Sm[MAname][i] - abs(wide)
        thickness[i] = abs(wide) 

            

        
    #SU = Sm[MAname].apply(lambda x: (1+0.25*SD) * x if (1+0.25*SD) * abs(x)>=epsilon else epsilon)
    #SL = Sm[MAname].apply(lambda x: (1-0.25*SD) * x if (1+0.25*SD) * abs(x)>=epsilon else -epsilon)
    try:
        transformed = pd.DataFrame(-np.log((SU - Si.iloc[:,0])/(SU - SL)) )
        #transformed_raw = pd.DataFrame(-np.log(((1+0.25*SD)*Sm[MAname]-Si.iloc[:,0])/(Sm[MAname]*(0.5*SD))))
    except RuntimeWarning:
        print('negative log encounted in ', params)
        with open(filepath["root"] + itemType + "errorList.txt", "a+") as f:
            f.writelines("{} {} {} {}\n".format(params[0], params[1], params[2],epsilon))
        warnings.simplefilter("default")
        transformed = pd.DataFrame(-np.log((SU - Si.iloc[:,0])/(SU - SL)) )
        #transformed_raw = pd.DataFrame(-np.log(((1+0.25*SD)*Sm[MAname]-Si.iloc[:,0])/(Sm[MAname]*(0.5*SD))))
    
    transformed.columns = ["bounded_x"]
    #transformed_raw.columns = ["bounded_x_raw"]

    table = pd.concat([Si, Sm, normalize,SU,SL,thickness,transformed], axis=1)
    colname = list(table.columns)
    colname[3] = "S_U"
    colname[4] = "S_L"
    table.columns = colname
    #table.rename(columns={ table.columns[4]: "S_U" }, inplace = True)
    transformed.to_csv(filepath["toanalysis"] + "bounded_" + filestring + names, sep=",", index=True)
    table.to_csv(filepath["table"] + filestring + names, sep=",", index=True)

        
        
def updateRaw(itemType,region):
    #sdList = [1.5,1.75,2,2.5]
    #dayList = [30,50,60,90,120]
    indexList = getItemNameFromJson(itemType,region)
    if "bond" not in itemType:
        extractRaw(indexList,itemType + region)
        print("extractRaw done")
    paramList = getParameterListFromJson(itemType,region)
    #paramList = (("0175.HK",2,30,"stockHK"),("0175.HK",2,60,"stockHK"),("0175.HK",2,90,"stockHK"),("0175.HK",2,120,"stockHK"))
    #print(paramList)
    for param in paramList:
        processRaw(param,itemType + region)

    print("processRaw done")
    return 0
    

if __name__ == '__main__':
    itemType, region = inputForm()
    updateRaw(itemType,region)
