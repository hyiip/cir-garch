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
from getIndexList import getIndexList

def plotlyPlot(df, varName, windowssize = 750, cond = 1):
    height = windowssize-1
    df = df.iloc[height:]
    
    df = df.fillna(0)
    
    if varName == "sigma":
        df['garch_' + varName].iloc[:height] = np.NaN
        df['garch_' + varName + '_se'].iloc[:height] = np.NaN
        df['garch_' + varName + '_z'].iloc[:height] = np.NaN

    df = df.replace(0,np.nan)
    garch_trace = go.Scatter(
        name='GARCH_' + varName,
        x=df.index.tolist(),
        y=df['garch_' + varName],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgba(31, 119, 180, 0.5)', width = 2)
        )



    cir_trace = go.Scatter(
        name='CIR_' + varName,
        x=df.index.tolist(),
        y=df['cir_' + varName],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgba(255, 127, 14, 0.5)', width = 2)
         )


    garch_se_trace = go.Scatter(
        name='GARCH_' + varName+"_se",
        x=df.index.tolist(),
        y=df['garch_' + varName + '_se'],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgba(148,103,189,0.5)', width = 2)
        )



    cir_sd_trace = go.Scatter(
        name='CIR_' + varName+"_se",
        x=df.index.tolist(),
        y=df['cir_' + varName + '_sd'],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgba(140,86,75,0.5)', width = 2)
         )
        
    garchz_trace = go.Scatter(
        name='GARCH_' + varName + "_zscore (right)",
        x=df.index.tolist(),
        y=df['garch_' + varName + '_z'],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        yaxis='y2',
        line=dict(color='#2ca02c', width = 2)
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
    if not cond and varName == "sigma":
        data = [cir_trace,cir_sd_trace,cirz_trace]
        #data = [cir_trace,cirz_trace]
    else:
        data = [garch_trace, cir_trace, garch_se_trace , cir_sd_trace, garchz_trace,  cirz_trace]
        #data = [garch_trace, cir_trace, garchz_trace,  cirz_trace]
    return data
    '''layout = go.Layout(
        yaxis=dict(title='Wind speed (m/s)'),
        title='Continuous, variable value error bars',
        legend=dict(orientation="h"))
    fig = go.Figure(data=data, layout=layout)'''
    
def errorPlot(params):

    SDint = params[0]
    day = params[1]
    index = params[2]
    mode = params[3]
    
    MA = str(day)
    SD = str(int(SDint*100))
    
    folderString = "SD{}/day{}/{}/".format(SD,MA,mode)
    
    originPath = "updating/result/{}".format(folderString)
    
    names = "day{}_SD{}_{}.csv".format(MA,SD,index)
        
    outputPath = "updating/plotly/zscore/{}/{}/".format(folderString,index)
    if not os.path.exists(outputPath): #for unknown reason, multiprocess does not support exist_ok = True
        Path(outputPath).mkdir(parents=True, exist_ok=True)
    
    condDataframe = pd.read_csv(originPath + names , usecols=[0,31], index_col=0, na_values=["null"])
    print("z stat")
    print(names)
    if condDataframe["garch_sigma"].sum()<0:
        sigmaCondition = 0 #if sigma<0
    else:
        sigmaCondition = 1
    firstDate = condDataframe.index[0]
    lastDate = condDataframe.index[-1]
    
    kappa_z = pd.read_csv(originPath + names , usecols=[0,6,7,10,11,12,15], index_col=0, na_values=["null"])
    theta_z = pd.read_csv(originPath + names , usecols=[0,16,17,20,21,22,25], index_col=0, na_values=["null"])
    sigma_z = pd.read_csv(originPath + names , usecols=[0,26,27,30,31,32,35], index_col=0, na_values=["null"])
    varList = ["kappa","theta","sigma"]
    dfList = [kappa_z,theta_z,sigma_z]
    #varList = ["sigma"]
    #dfList = [sigma]
    
    
    for varName, dfName in zip(varList, dfList):
        titlestring = "{}_MA{}_SD{}_{}_{} error plot ({} to {})".format(mode,MA,SDint,index,varName, firstDate, lastDate)
        data = plotlyPlot(df=dfName, varName=varName,cond = sigmaCondition)
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
    
        
    
def zstatPlot():
    start = time.time()
    dayList = [30,50,60,90,120]
    sdList = [1.75,2]
    indexList = getIndexList()
    modeList = ["roll","expand"]
    paramList = list(itertools.product(sdList,dayList,modeList,indexList))
    
    #for param in paramList:
    #    errorPlot(param)
    cpuCount = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpuCount-1)
    pool.map(errorPlot,paramList)
    
    end = time.time()
    elapsed = end - start
    print("time used: " + str(elapsed))
        
if __name__ == '__main__':
    zstatPlot()