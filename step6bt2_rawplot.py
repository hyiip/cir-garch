import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import plotly
import plotly.graph_objs as go
import plotly.io as pio

import multiprocessing
import time

import itertools
from garch_utils.getList import getParameterListFromJson
from garch_utils.inputForm import inputForm

    
def infoPlot(params):

    item = params[0]
    SDint = params[1]
    day = params[2]
    itemType = params[3]
    mode = params[4]
    
    MA = str(day)
    SD = str(int(SDint*100))
    
    folderString = "SD{}/day{}/".format(SD,MA)
    
    
    originPath = itemType + "/updating/table/{}".format(folderString)
    
    names = "day{}_SD{}_{}.csv".format(MA,SD,item)
        
    outputPath = itemType + "/updating/plotly/raw/{}/{}/".format(folderString,item)
    
    if not os.path.exists(outputPath): #for unknown reason, multiprocess does not support exist_ok = True
        Path(outputPath).mkdir(parents=True, exist_ok=True)
        
    infoDF = pd.read_csv(originPath + names , usecols=[0,1,2,3,4], index_col=0, na_values=["null"])
    firstDate = infoDF.index[0]
    lastDate = infoDF.index[-1]
    
    infoTitle = "{}_{} normalized index & y (SD = {}) from {} to {}".format(itemType,item,SDint, firstDate, lastDate)
    colName = infoDF.columns[0]
    close_trace = go.Scatter(
        name=item,
        x=infoDF.index.tolist(),
        y=infoDF[colName],
        hoverlabel = dict(namelength = -1),
        mode='lines' )
    ma_trace = go.Scatter(
        name=MA + "MA",
        x=infoDF.index.tolist(),
        y=infoDF[MA + "MA"],
        hoverlabel = dict(namelength = -1),
        mode='lines' )
    normalize_trace = go.Scatter(
        name = "{}/{}MA (Left)".format(colName,MA),
        x=infoDF.index.tolist(),
        y=infoDF["Normalize"],
        hoverlabel = dict(namelength = -1),
        line=dict(color='rgba(31, 119, 180,1)'),
        mode='lines',
        yaxis='y2'
        )
    bounded_trace = go.Scatter(
        name="y (Right)",
        x=infoDF.index.tolist(),
        y=infoDF["bounded_x"],
        hoverlabel = dict(namelength = -1),
        line=dict(color='rgba(255, 127, 14,0.8)'),
        mode='lines' )

    data1 = [close_trace, ma_trace]
    data2 = [normalize_trace, bounded_trace]
    layout1 = go.Layout(
        yaxis=dict(rangemode='nonnegative',tickformat=",d"),
        title=item,
        legend=dict(orientation="h"))
    fig1 = go.Figure(data=data1, layout=layout1)
    
    layout2 = go.Layout(
        title=infoTitle,
        legend=dict(orientation="h"),
        yaxis=dict(
            side='right',
            showgrid=False,
            showline=False
        ),
        yaxis2 = dict(
            overlaying='y'),
        shapes= [
            # Line Horizontal
            {
                'type': 'line',
                'x0': str(firstDate),
                'y0': 1-0.25*SDint,
                'x1': str(lastDate),
                'y1': 1-0.25*SDint,
                'yref': 'y2',
                'line': {
                    'color': 'green','dash': 'dot'
                },
            }
        ])
    fig2 = go.Figure(data=data2, layout=layout2)
    indexDiv = plotly.offline.plot(fig1, include_plotlyjs=False, show_link=False, output_type='div')
    normalizeDiv = plotly.offline.plot(fig2, include_plotlyjs=False, show_link=False, output_type='div')
    
    with open(outputPath + "index.html", 'w') as f:
        print(outputPath)
        f.write(indexDiv)    
    with open(outputPath + "normalize.html", 'w') as f:
        f.write(normalizeDiv)    
    

def callInfoPlot(itemType , region):
    start = time.time()
    tempList = getParameterListFromJson(itemType,region)
    modeList = ["expand","roll"]
    paramList = [(*a,b) for a,b in itertools.product(tempList,modeList)]

    
    #for param in paramList:
    #    infoPlot(param)
    cpuCount = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpuCount-1)
    pool.map(infoPlot,paramList)
    
    end = time.time()
    elapsed = end - start
    print("time used: " + str(elapsed))
    return 0

if __name__ == '__main__':
    itemType, region = inputForm()
    callInfoPlot(itemType , region)