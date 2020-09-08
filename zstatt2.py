import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import plotly
import plotly.graph_objs as go

import multiprocessing
import time

import itertools
from garch_utils.getList import getParameterListFromJson

def plotlyPlot(df, varName, windowssize = 750, cond = 1):
    height = windowssize-1
    df = df.iloc[height:]
    
    df = df.fillna(0)

    df = df.replace(0,np.nan)

    cir_trace = go.Scatter(
        name='CIR_' + varName,
        x=df.index.tolist(),
        y=df['cir_' + varName],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgba(255, 127, 14, 0.5)', width = 2)
         )


    cir_sd_trace = go.Scatter(
        name='CIR_' + varName+"_se",
        x=df.index.tolist(),
        y=df['cir_' + varName + '_sd'],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgba(140,86,75,0.5)', width = 2)
         )
                 
    cirz_trace = go.Scatter(
        name='CIR_' + varName + "_zscore (right)",
        x=df.index.tolist(),
        y=df['cir_' + varName + '_z'],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        yaxis='y2',
        line=dict(color='#d62728', width = 2)
         )
    # Trace order can be important
    # with continuous error bars
    data = [cir_trace,cir_sd_trace,cirz_trace]
    return data
    '''layout = go.Layout(
        yaxis=dict(title='Wind speed (m/s)'),
        title='Continuous, variable value error bars',
        legend=dict(orientation="h"))
    fig = go.Figure(data=data, layout=layout)'''
    
def errorPlot(params):

    item = params[0]
    SDint = params[1]
    day = params[2]
    itemType = params[3]
    mode = params[4]

    MA = str(day)
    SD = str(int(SDint*100))
    
    folderString = "SD{}/day{}/{}/".format(SD,MA,mode)
    
    originPath = itemType + "/updating/result/{}".format(folderString)
    
    names = "day{}_SD{}_{}.csv".format(MA,SD,item)
        
    outputPath = "{}/updating/plotly/zscore/{}/{}/".format(itemType,folderString,item)
    if not os.path.exists(outputPath): #for unknown reason, multiprocess does not support exist_ok = True
        Path(outputPath).mkdir(parents=True, exist_ok=True)
    
    condDataframe = pd.read_csv(originPath + names , usecols=[0,6], index_col=0, na_values=["null"])
    print("z stat")
    print(names)
    firstDate = condDataframe.index[0]
    lastDate = condDataframe.index[-1]
    
    kappa_z = pd.read_csv(originPath + names , usecols=[0,6,7,10], index_col=0, na_values=["null"])
    theta_z = pd.read_csv(originPath + names , usecols=[0,11,12,15], index_col=0, na_values=["null"])
    sigma_z = pd.read_csv(originPath + names , usecols=[0,16,17,20], index_col=0, na_values=["null"])
    varList = ["kappa","theta","sigma"]
    dfList = [kappa_z,theta_z,sigma_z]
    #varList = ["sigma"]
    #dfList = [sigma]
    
    
    for varName, dfName in zip(varList, dfList):
        titlestring = "{}_{}_MA{}_SD{}_{}_{} error plot ({} to {})".format(itemType,mode,MA,SDint,item,varName, firstDate, lastDate)
        data = plotlyPlot(df=dfName, varName=varName)
        layout = go.Layout(
            yaxis=dict(title=varName,rangemode='nonnegative'),
            title=titlestring,
            legend=dict(orientation="h"),
            yaxis2=dict(
                overlaying='y',
                title="z-score",
                side='right',
                showgrid=False,
                showline=False
        ))
        fig = go.Figure(data=data, layout=layout)
        '''plotly.offline.plot(fig, filename=outputPath + varName + ".html", auto_open=False)'''
        
        aPlot = plotly.offline.plot(fig, include_plotlyjs=False, show_link=False, output_type='div')
        with open(outputPath + varName + ".html", 'w') as f:
            f.write(aPlot)
    print(outputPath)
    

def zstatPlot(itemType , region):
    start = time.time()
    tempList = getParameterListFromJson(itemType,region)
    modeList = ["expand","roll"]
    paramList = [(*a,b) for a,b in itertools.product(tempList,modeList)]

    cpuCount = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpuCount-1)
    pool.map(errorPlot,paramList)
    
    end = time.time()
    elapsed = end - start
    print("time used: " + str(elapsed))
        
if __name__ == '__main__':
    region = ""
    print("input item type (stock/index/bond)")
    itemType = input().strip()
    if itemType == "stock":
        print("input item region eg.(US/HK)")
        region = input().strip()
    if itemType == "bond":
        print("input item region eg.(GER)")
        region = input().strip()
    zstatPlot(itemType , region)
    