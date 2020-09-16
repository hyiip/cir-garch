#from kaleido.scopes.plotly import PlotlyScope
#import plotly.graph_objects as go
#scope = PlotlyScope()
import matplotlib.pyplot as plt
import itertools
import multiprocessing
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

from pathlib import Path
from garch_utils.getList import getItemNameFromJson,getParameterListFromJson
from garch_utils.inputForm import inputForm
figsize=(16, 8)
fontsize = 16
def plotGraphSetting(params,result,setting,itemmode):
    mode = params[0]
    item = params[1]
    SD = params[2]
    MA = params[3]
    itemType = params[4]
    try:
        epsilon = float(params[5])
    except:
        epsilon = 0
    '''column name: [result.columns[0],MA+"MA","Bank's Rate","S/S_A", "S_U", "S_L", "Band Width", "s","Leakage Ratio",
        "kappa","kappa_SE","kappa_lb","kappa_ub","kappa_z",
        "theta","theta_SE","theta_lb","theta_ub","theta_z",
        "sigma","sigma_SE","sigma_lb","sigma_ub","sigma_z"]'''
    if itemType == "exchange":
        suffix = ""
        item = item[:3] + "/" + item[3:]
    elif epsilon != 0:
        suffix = "(SD = {}, MA = {}, Tolerance  = {})".format(SD, MA, epsilon)
    else:
        suffix = "(SD = {}, MA = {})".format(SD, MA)
    if itemmode == "upper":
        title = {
            "stdtit": "{}, moving average and quasi-bounded fixed at S_U {}".format(item, suffix),
            "leakage": "{} and leakage ratio {}".format(item, suffix),
            "normalize": "{} and S/S_A {}".format(item, suffix),
            "s": "{} and s {}".format(item, suffix),}
    elif itemmode == "lower":
        title = {
            "stdtit": "{}, moving average, quasi-bounded fixed at zero {}".format(item, suffix),
            "leakage": "{} and leakage ratio {}".format(item, suffix),
            "normalize": "{} and S/S_A {}".format(item, suffix),
            "s": "{} and s {}".format(item, suffix),}
    elif itemType == "exchange":
        title = {
            "stdtit": "{}, strong side and weak side {}".format(item, suffix),
            "leakage": "{} and leakage ratio {}".format(item, suffix),
            "normalize": "{} and S/S_A {}".format(item, suffix),
            "s": "{} and s {}".format(item, suffix),}
    else:
        title = {
            "stdtit": "{}, moving average, S_U and S_L {}".format(item, suffix),
            "leakage": "{} and leakage ratio {}".format(item, suffix),
            "normalize": "{} and S/S_A {}".format(item, suffix),
            "s": "{} and s {}".format(item, suffix),}
    if setting == "main":
        if "bond" in itemType:
            if itemmode in ["upper","lower"]:
                data = result[[result.columns[0], "{}MA".format(MA),"S_U"]]
            else:
                data = result[[result.columns[0], "{}MA".format(MA),"S_U", "S_L"]]
        elif itemType == "exchange":
            data = result[[result.columns[0]]]
            if item == "HKD/USD":
                upper = data.copy()*0 + 1/7.75
                upper = upper.rename(columns={"Close": "Weak side"})
                lower = data.copy()*0 + 1/7.85
                lower = lower.rename(columns={"Close": "Strong side"})
            elif item == "USD/HKD":
                upper = data.copy()*0 + 7.85
                upper = upper.rename(columns={"Close": "Weak side"})
                lower = data.copy()*0 + 7.75
                lower = lower.rename(columns={"Close": "Strong side"})
            data = pd.concat([data, upper, lower],axis = 1)
            print(data)
        else:
            data = result[[result.columns[0], "{}MA".format(MA),"S_U", "S_L"]]
        ax1 = data.plot(title = title["stdtit"], grid=True, fontsize=fontsize, figsize=figsize, xticks = (np.arange(0, len(data)+1, 250.0)))

    if setting == "s":
        data = result[[result.columns[0], "s"]]
        ax1 = data.plot(title = title[setting], grid=True, fontsize=fontsize, secondary_y="s", figsize=(16, 8), xticks = (np.arange(0, len(data)+1, 250.0)))

        ax1.right_ax.set_ylabel("s", fontsize = fontsize)

    if setting == "leakage":
        data = result[[result.columns[0], "Leakage Ratio"]]
        ax1 = data.plot(title = title[setting], grid=True, fontsize=fontsize, secondary_y="Leakage Ratio", figsize=(16, 8), xticks = (np.arange(0, len(data)+1, 250.0)))

        ax1.right_ax.set_ylabel("Leakage Ratio", fontsize = fontsize)
        if max(result["Leakage Ratio"]>1):
            ax1.right_ax.set_ylim(0,1.5)

    if setting == "normalize":
        data = result[[result.columns[0], "S/S_A"]]
        ax1 = data.plot(title = title[setting], grid=True, fontsize=fontsize, secondary_y="S/S_A", figsize=(16, 8), xticks = (np.arange(0, len(data)+1, 250.0)))

        ax1.right_ax.set_ylabel("S/S_A", fontsize = fontsize)
        ax1.right_ax.set_ylim(0,4)
    if "bond" in itemType:
        ylabalT = "Bond Yield"
    elif "vix" in itemType:
        ylabalT = "VIX"
    elif itemType == "exchange":
        ylabalT = item
    else:
        ylabalT = ""
    ax1.set_ylabel(ylabalT, fontsize = fontsize)
    ax1.set_xlabel("Date", fontsize = fontsize)
    ax1.title.set_fontsize(fontsize)
    for item in (ax1.get_legend().get_texts()):
        item.set_fontsize(fontsize)
    plt.autoscale(enable=True, axis='x', tight=True)
    fig1 = ax1.get_figure()
    fig1.autofmt_xdate()
    plt.close('all')
    return fig1
def plotGraphParameter(params,result,parameter,itemmode):
    mode = params[0]
    item = params[1]
    SD = params[2]
    MA = params[3]
    itemType = params[4]
    try:
        epsilon = float(params[5])
    except:
        epsilon = 0
    '''column name: [result.columns[0],MA+"MA","Bank's Rate","S/S_A", 'S_U', 'S_L', 'Band Width', "s","Leakage Ratio",
        "kappa","kappa_SE","kappa_lb","kappa_ub","kappa_z",
        "theta","theta_SE","theta_lb","theta_ub","theta_z",
        "sigma","sigma_SE","sigma_lb","sigma_ub","sigma_z"]'''
    data = result[[parameter, parameter + "_z"]]
    data["z-score > 1.96"] = 1.96
    data = data.iloc[749:]
    if itemType == "exchange":
        suffix = ""
        item = item[:3] + "/" + item[3:]
    elif epsilon != 0:
        suffix = "(SD = {}, MA = {}, Tolerance  = {})".format(SD, MA, epsilon)
    else:
        suffix = "(SD = {}, MA = {})".format(SD, MA)

    if itemmode == "upper":
        title = "{}ing windows, quasi-bounded fixed at S_U, {} - {} and z-score {}".format(mode.capitalize(),item, parameter, suffix)
    elif itemmode == "lower":
        title = "{}ing windows, quasi-bounded fixed at zero, {} - {} and z-score {}".format(mode.capitalize(),item, parameter, suffix)
    else:
        title = "{}ing windows, {} - {} and z-score {}".format(mode.capitalize(),item, parameter, suffix)

    '''varMain = go.Scatter(
        name=parameter,
        x=data.index.tolist(),
        y=data[parameter],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        line=dict(color='rgb(31, 119, 180)'),
        )
    zPlot = go.Scatter(
        name=parameter + "_zscore (right)",
        x=data.index.tolist(),
        y=data[parameter + "_z"],
        hoverlabel = dict(namelength = -1),
        mode='lines',
        yaxis='y2',
        line=dict(color='rgb(255, 127, 14)', width = 2),
         )
    plotData = [varMain,zPlot]
    layout = go.Layout(
            yaxis=dict(title=parameter, rangemode='nonnegative',
                showgrid=True,
                showline=True,
                gridcolor='rgb(0, 0, 0)',),
            title=title,
            legend=dict(orientation="h"),
            yaxis2=dict(
                overlaying='y',
                side='right',
                showgrid=False,
                showline=False,
                title = "z score",
            ),
            xaxis_title="Date",
            template="plotly_white",
            )
    fig = go.Figure(data=plotData, layout=layout)'''
    ax1 = data.plot(title =  title, grid=True, secondary_y=["{}_z".format(parameter),"z-score > 1.96"], fontsize=fontsize,figsize=(16, 8), xticks = (np.arange(0, len(data)+1, 250.0)))
    plt.autoscale(enable=True, axis='x', tight=True)                           
    ax1.set_xlabel("Date", fontsize = fontsize)
    ax1.set_ylabel(parameter, fontsize = fontsize)
    ax1.right_ax.set_ylabel("z score", fontsize = fontsize)
    ax1.title.set_fontsize(fontsize)
    for item in (ax1.get_legend().get_texts()):
        item.set_fontsize(fontsize)
    fig1 = ax1.get_figure()
    fig1.autofmt_xdate()
    return fig1

def relabelAndPlot(params):
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
    pathString = "SD{}/day{}/{}/".format(SD,MA,mode)
    itemmode = itemType.replace("bond","").replace("GER","")
    if itemmode not in ["upper","lower"]:
        itemmode = ""
    else:
        itemmode =  itemmode
    
    if not epsilon == 0:
        filepath = {
            "graph": "{itemType}/updating/graph/{item}/SD{SDint}day{day}tol{epsilon}/{mode}/".format(itemType = itemType,item = item,SDint = SDint,day = day,epsilon = epsilon,mode = mode),
            "result": "{}/updating/tor{}/result/SD{}/day{}/{}/".format(itemType,epsilon,SD,day,mode),
            "output_graph": "output/{itemType}/graph/{item}/day{day}tol{epsilon}SD{SDint}/{mode}/".format(itemType = itemType,item = item,SDint = SDint,day = day,epsilon = epsilon,mode = mode),
            "output_result": "output/{itemType}/result/{item}/day{day}tol{epsilon}SD{SDint}/{mode}/".format(itemType = itemType,item = item,SDint = SDint,day = day,epsilon = epsilon,mode = mode),
            }
        resultFile =  "tor{}_day{}_SD{}_{}.csv".format(epsilon,MA,SD,item)
        graphName = "{}_SD{}day{}tol{}".format(item,SDint,day,epsilon)
        infographName = "{}_SD{}day{}tol{}".format(item,SDint,day,epsilon)
    else:
        if not "exchange" == itemType:
            filepath = {
                "graph": "{itemType}/updating/graph/{item}/SD{SDint}day{day}/{mode}/".format(itemType = itemType,item = item,SDint = SDint,day = day,mode = mode),
                "result": "{itemType}/updating/result/SD{SD}/day{day}/{mode}/".format(itemType = itemType,SD = SD,day = day,mode = mode),
                "output_graph": "output/{itemType}/graph/{item}/day{day}SD{SDint}/{mode}/".format(itemType = itemType,item = item,SDint = SDint,day = day,mode = mode),
                "output_result": "output/{itemType}/result/{item}/day{day}SD{SDint}/{mode}/".format(itemType = itemType,item = item,SDint = SDint,day = day,mode = mode),
                }
        else:
            filepath = {
                "graph": "{itemType}/updating/graph/{item}/SD{SDint}day{day}/{mode}/".format(itemType = itemType,item = item,SDint = SDint,day = day,mode = mode),
                "result": "{itemType}/updating/result/SD{SD}/day{day}/{mode}/".format(itemType = itemType,SD = SD,day = day,mode = mode),
                "output_graph": "output/{itemType}/graph/{item}/{mode}/".format(itemType = itemType,item = item,mode = mode),
                "output_result": "output/{itemType}/result/{item}/{mode}/".format(itemType = itemType,item = item,mode = mode),
                }

        if "bond" not in itemType:
            resultFile = "{}_day{}_SD{}_{}.csv".format(mode,MA,SD,item)
            graphName = "{}_{}_SD{}day{}".format(mode,item,SDint,day)
            infographName = "{}_SD{}day{}".format(item,SDint,day)
        elif "exchange" in itemType:
            resultFile = "{}_day{}_SD{}_{}.csv".format(mode,MA,SD,item)
            graphName = "{}_{}".format(mode,item)
            infographName = "{}".format(item)
        else:
            resultFile = "{}_{}_day{}_SD{}_{}.csv".format(mode,itemmode,MA,SD,item)
            graphName = "{}_{}_{}_SD{}day{}".format(mode,itemmode,item,SDint,day)
            infographName = "{}_{}_SD{}day{}".format(itemmode,item,SDint,day)
    for f in filepath.values():
        tempPath = Path(f)
        tempPath.mkdir(parents=True, exist_ok=True)
    resultPath = filepath["result"] + resultFile
    #bank = pd.read_csv("{}/updating/bank.csv".format(itemType) , index_col=0, na_values=["null"])
    #bank = bank.drop(bank.index[0:day-1])
    result = pd.read_csv(resultPath, index_col=0)
    result.to_csv(filepath["output_result"] + resultFile, sep=",", index=True)
    #result.insert(2,"Bank",bank["Bank"].tolist())
    '''
    result.columns = [result.columns[0],MA+"MA","Bank's Rate","S/S_A", 'S_U', 'S_L', 'Band Width', "s","Leakage Ratio",
        "kappa","kappa_SE","kappa_lb","kappa_ub","kappa_z",
        "theta","theta_SE","theta_lb","theta_ub","theta_z",
        "sigma","sigma_SE","sigma_lb","sigma_ub","sigma_z"]
    '''
    #result.to_csv(resultPath, sep=",", index=True)
    
    variables = ["kappa", "theta", "sigma"]
    for var in variables:
        fig = plotGraphParameter(params,result, var,itemmode)
        fig.savefig(filepath["graph"] + "{}_{}.png".format(graphName,var) )
        fig.savefig(filepath["output_graph"] + "{}_{}.png".format(graphName,var) )
        fig.savefig(filepath["output_graph"] + "{}_{}.eps".format(graphName,var), format='eps' )
    
    if itemType == "exchange":
        setting = ["main","s","leakage"]
    else:
        setting = ["main","s","leakage","normalize"]
    
    for var in setting:
        fig = plotGraphSetting(params,result, var,itemmode)
        fig.savefig(filepath["graph"] + "{}_{}.png".format(infographName,var) )
        fig.savefig(filepath["output_graph"] + "{}_{}.png".format(infographName,var) )
        fig.savefig(filepath["output_graph"] + "{}_{}.eps".format(infographName,var), format='eps' )
    print(params)
    '''
    lws = [1.5, 2, 1.25]
    mu = pd.read_csv("result/rolling_3000_result/" + names , usecols=[0,1,2,3], index_col=0, na_values=["null"])
    sigma = pd.read_csv("result/rolling_3000_result/" + names , usecols=[0,4,5,6], index_col=0, na_values=["null"])
    
    mutitle = "roll_3000_" + names[:4] + "." + names[4:6] + "_mu"
    sigmatitle = "roll_3000_" + names[:4] + "." + names[4:6] + "_sigma"
    
    ax1 = mu.plot(title =  mutitle, grid=True, secondary_y="mu_z", figsize=(16, 8), xticks = (np.arange(0, len(mu)+1, 100.0)))
    plt.autoscale(enable=True, axis='x', tight=True)   
    ax2 = sigma.plot(title = sigmatitle, grid=True, secondary_y="sigma_z", figsize=(16, 8), xticks = (np.arange(0, len(mu)+1, 100.0)))
    for i, l in enumerate(ax1.lines):
        plt.setp(l, linewidth=lws[i])
        
    for i, l in enumerate(ax2.lines):
        plt.setp(l, linewidth=lws[i])                                         
                     
    plt.autoscale(enable=True, axis='x', tight=True)   
    fig1 = ax1.get_figure()
    fig1.autofmt_xdate()
    fig1.savefig("img/roll_3000/mu/" + mutitle + ".png")
    fig2 = ax2.get_figure()
    fig2.autofmt_xdate()
    fig2.savefig("img/roll_3000/sigma/" + sigmatitle + ".png")
    plt.close('all')
    '''
    

def tablePlot(params):
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
    pathString = "SD{}/day{}/{}/".format(SD,MA,mode)
    itemmode = itemType.replace("bond","").replace("GER","")
    if itemmode not in ["upper","lower"]:
        itemmode = ""
    else:
        itemmode =  itemmode
    
    if not epsilon == 0:
        filepath = {
            "graph": "{itemType}/updating/graph/{item}/SD{SDint}day{day}tol{epsilon}/".format(itemType = itemType,item = item,SDint = SDint,day = day,epsilon = epsilon),
            "table": "{itemType}/updating/tor{epsilon}/table/SD{SD}/day{day}/".format(itemType = itemType,epsilon = epsilon,SD = SD,day = day),
            "output_graph": "output/{itemType}/graph/{item}/day{day}tol{epsilon}SD{SDint}/".format(itemType = itemType,item = item,SDint = SDint,day = day,epsilon = epsilon),
            "output_table": "output/{itemType}/table/{item}/day{day}tol{epsilon}SD{SDint}/".format(itemType = itemType,item = item,SDint = SDint,day = day,epsilon = epsilon),
            }
        tableFile =  "tor{}_day{}_SD{}_{}.csv".format(epsilon,MA,SD,item)
        graphName = "{}_SD{}day{}tol{}".format(item,SDint,day,epsilon)
        infographName = "{}_SD{}day{}tol{}".format(item,SDint,day,epsilon)
    else:
        filepath = {
            "graph": "{itemType}/updating/graph/{item}/SD{SDint}day{day}/".format(itemType = itemType,item = item,SDint = SDint,day = day),
            "table": "{itemType}/updating/table/SD{SD}/day{day}/".format(itemType = itemType,SD = SD,day = day),
            "output_graph": "output/{itemType}/graph/{item}/day{day}SD{SDint}/".format(itemType = itemType,item = item,SDint = SDint,day = day),
            "output_table": "output/{itemType}/table/{item}/day{day}SD{SDint}/".format(itemType = itemType,item = item,SDint = SDint,day = day),
            }
        tableFile = "day{}_SD{}_{}.csv".format(MA,SD,item)
        graphName = "{}_SD{}day{}".format(item,SDint,day)
        infographName = "{}_SD{}day{}".format(item,SDint,day)
    for f in filepath.values():
        tempPath = Path(f)
        tempPath.mkdir(parents=True, exist_ok=True)
    talbePath = filepath["table"] + tableFile
    table = pd.read_csv(talbePath, index_col=0)
    table.columns = [table.columns[0],MA+"MA","S/S_A", 'S_U', 'S_L', "s"]
    table.to_csv(filepath["output_table"] + tableFile, sep=",", index=True)
    setting = ["VIX", "s", "normalize"]
    for var in setting:
        fig = plotGraphSetting(params,table, var,itemmode)
        fig.savefig(filepath["graph"] + "{}_{}.png".format(infographName,var) )
        fig.savefig(filepath["output_graph"] + "{}_{}.png".format(infographName,var) )
    print(params)
    

def merger(itemType , region,mode="hybrid"):
    tempList = getParameterListFromJson(itemType,region,mode = "plot")
    modeList = ["roll"]
    paramList = [(a,*b) for a,b in itertools.product(modeList,tempList)]

    cpuCount = multiprocessing.cpu_count()
    #print(cpuCount)
    #pool = multiprocessing.Pool(processes=cpuCount)
    #pool.map(relabelAndPlot,paramList)
    for param in paramList:
        relabelAndPlot(param)
    return 0
        
if __name__ == '__main__':
    #itemType, region = inputForm()
    for mode in ["default"]:
        itemType = "exchange"
        region = ""
        #itemType = "vixir"
        #region = ""
        merger(itemType,region, mode = mode)
    #itemType = "bondfloat3"
    #region = "GER"
    #merger(itemType , region)