import pandas as pd
import numpy as np
from os import listdir
import os
from os.path import isfile, join
from pathlib import Path
import plotly
import plotly.graph_objs as go
import multiprocessing
import time

import itertools
from garch_utils.getList import getParameterListFromJson
from garch_utils.inputForm import inputForm
from zstatt2 import errorPlot

def plotlyPlot(df, varName, windowssize = 750, cond = 1):
    height = windowssize-1
    df = df.iloc[height:]

    df = df.fillna(0)


    cir_upper_bound = go.Scatter(
        name='CIR ' + varName + ' Upper Bound',
        x=df.index.tolist(),
        y=df['cir_' + varName + '_ub'],
        showlegend=False,
        hoverlabel = dict(namelength = -1),
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        fillcolor='rgba(255, 127, 14, 0.3)',
        fill='tonexty' )

    cir_trace = go.Scatter(
        name='CIR_' + varName,
        x=df.index.tolist(),
        y=df['cir_' + varName],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgb(255, 127, 14)')
         )

    cir_lower_bound = go.Scatter(
        name='CIR ' + varName + ' Lower Bound',
        x=df.index.tolist(),
        y=df['cir_' + varName + '_lb'],
        showlegend=False,
        hoverlabel = dict(namelength = -1),
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines' )

    leakage_trace = go.Scatter(
        name='CIR_leakage',
        x=df.index.tolist(),
        y=df['cir_leakage'],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgb(165, 165, 165)'),
        yaxis='y2'
         )
    # Trace order can be important
    # with continuous error bars
    data = [cir_lower_bound, cir_upper_bound, cir_trace,leakage_trace]
    return data
    '''layout = go.Layout(
        yaxis=dict(title='Wind speed (m/s)'),
        title='Continuous, variable value error bars',
        legend=dict(orientation="h"))
    fig = go.Figure(data=data, layout=layout)'''

def indexPlot(params):

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

    outputPath = itemType + "/updating/plotly/{}{}/".format(folderString,item)
    if not os.path.exists(outputPath): #for unknown reason, multiprocess does not support exist_ok = True
        Path(outputPath).mkdir(parents=True, exist_ok=True)

    condDataframe = pd.read_csv(originPath + names , usecols=[0,6], index_col=0, na_values=["null"])
    print(names)
    firstDate = condDataframe.index[0]
    lastDate = condDataframe.index[-1]

    kappa = pd.read_csv(originPath + names , usecols=[0,5,6,8,9], index_col=0, na_values=["null"])
    theta = pd.read_csv(originPath + names , usecols=[0,5,11,13,14], index_col=0, na_values=["null"])
    sigma = pd.read_csv(originPath + names , usecols=[0,5,16,18,19], index_col=0, na_values=["null"])
    varList = ["kappa","theta","sigma"]
    dfList = [kappa,theta,sigma]
    #varList = ["sigma"]
    #dfList = [sigma]


    for varName, dfName in zip(varList, dfList):
        titlestring = "{}_{}_MA{}_SD{}_{}_{} ({} to {})".format(itemType,mode,MA,SDint,item,varName, firstDate, lastDate)
        cirdiff = (dfName['cir_' + varName + '_ub']- dfName['cir_' + varName])
        cir25sd = (cirdiff.quantile(0.97) )/1.96*2.5
        circhmax =  cir25sd + dfName['cir_' + varName].quantile(0.97)
        circhmin =  -cir25sd + dfName['cir_' + varName].quantile(0.03)
        yrangemax = circhmax
        yrangemin = max(0, circhmin)
        data = plotlyPlot(df=dfName, varName=varName)
        if varName == "sigma":
            layout = go.Layout(
                yaxis=dict(title=varName, rangemode='nonnegative'),
                title=titlestring,
                legend=dict(orientation="h"),
                yaxis2=dict(
                    overlaying='y',
                    side='right',
                    showgrid=False,
                    showline=False,
                    range=[0, 1]
                ))
        else:
            layout = go.Layout(
                yaxis=dict(title=varName, rangemode='nonnegative', range=[yrangemin, yrangemax]),
                title=titlestring,
                legend=dict(orientation="h"),
                yaxis2=dict(
                    overlaying='y',
                    side='right',
                    showgrid=False,
                    showline=False,
                    range=[0, 1]
                ))
        fig = go.Figure(data=data, layout=layout)
        '''plotly.offline.plot(fig, filename=outputPath + varName + ".html", auto_open=False)'''

        aPlot = plotly.offline.plot(fig, include_plotlyjs=False, show_link=False, output_type='div')
        with open(outputPath + varName + ".html", 'w') as f:
            f.write(aPlot)
    print("index")
    print(outputPath)

def indexPlotMode(params):
    plotType = params[5]
    if plotType == "normal":
        indexPlot(params)
    elif plotType == "z":
        errorPlot(params)

def callPlotly(itemType , region):


    start = time.time()
    tempList = getParameterListFromJson(itemType,region)
    modeList = ["expand","roll"]
    plotType = ["normal","z"]
    paramList = [(*a,b,c) for a,b,c in itertools.product(tempList,modeList,plotType)]

    #for param in paramList:
    #    indexPlotMode(param)
    cpuCount = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpuCount-1)
    pool.map(indexPlotMode , paramList)

    end = time.time()
    elapsed = end - start
    print("time used: " + str(elapsed))
    return 0

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
    callPlotly(itemType , region)