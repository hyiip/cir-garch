import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import time
from functools import reduce

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["figure.figsize"] = (12,15)
plt.rcParams.update({'font.size': 16})
#plt.rcParams.update({'font.size': 16})
#inr = pd.read_csv("output/bondlowerUS/result/ust10yyield/day30SD2/roll/roll_lower_day30_SD200_ust10yyield.csv",index_col=0)
#inr = pd.read_csv("paper/bond/roll_lower_day30_SD800_F91010Y_no_max.csv",index_col=0)
#inr = pd.read_csv("paper/bond/roll_lower_day30_SD200_ust10yyield.csv",index_col=0)
#print(inr)

# t = inr.index.values


# s1 = inr["s"].to_numpy() 
# s2 = inr[inr.columns[0]].to_numpy() 
# s3 = inr["S_U"].to_numpy() 
# t = [dt.datetime.strptime(date, "%d/%m/%Y") for date in t]
#print(t)
# plt.scatter(x, y)
# plt.show()

fig, axs = plt.subplots(nrows = 2)
fig.subplots_adjust(hspace=0.4)

prefix = "paper/bond/update/"
#GER_Yield = pd.read_csv(prefix + "F91010Y.csv",index_col=0)
#CDS = pd.read_csv(prefix + "cds.csv",index_col=0)
#GER_res = pd.merge(left=GER_Yield, right=CDS, left_index=True, right_index=True)
#print(GER_res)
US_res = pd.read_csv(prefix + "US_cointegration.csv",index_col=0)

secaxs = [ax.twinx() for ax in axs]
#inr[inr.columns[0]].plot(ax = secax, linestyle="dashed", color = "red" ,label="yield (right)", linewidth = 1)
# lplot1 = GER_res["F91010Y"].plot(
#     ax = axs[0] , label="10Y GER Gov. Bond Yield (left)", linewidth = 1.5,
#     xticks = np.arange(0, len(GER_res)+1, 500.0))
# rplot1 =GER_res["cds"].plot(
#     ax = secaxs[0] ,linestyle="dashdot", color = "red", label="ITA Sovereign CDS Spread (right)", linewidth = 1.5)
#axs.set_xticks(np.arange(0, len(inr)+1, 250.0))
lplot2 =US_res["UST10YYIELD"].plot(
    ax = axs[0] , color = "brown",label="10Y US Treasury Yield (left)", linewidth = 2)
rplot2 =US_res["log_VIX"].plot(
    ax = secaxs[0] , linestyle="dashdot", color = "green",label="ln(VIX) (right)", linewidth = 1.5)
lplot3 =US_res["UST10YYIELD"].plot(
    ax = axs[1] ,color = "brown", label="10Y US Treasury Yield (left)", linewidth = 2)
#print(US_res["EPU"])
rplot3 =US_res["log_EPU"].plot(
    ax = secaxs[1] , linestyle="dashdot", color = "grey",label="ln(EPU) (right)", linewidth = 1.5)

axs[0].xaxis.set_tick_params(labelbottom=True)
axs[1].xaxis.set_tick_params(labelbottom=True)
#axs[2].xaxis.set_tick_params(labelbottom=True)
axs[1].xaxis.label.set_visible(False)
pTitle = ["10Y US Treasury Yield","10Y US Treasury Yield"]
sTitle = ["ln(VIX)","ln(EPU)"]

for ax, title in zip(axs,pTitle):
    ax.set_ylabel(title)

for ax, title in zip(secaxs,sTitle):
    ax.set_ylabel(title)

#handles, labels = [(a + b) for a, b in zip(axs.get_legend_handles_labels(),secaxs.get_legend_handles_labels() )]
for pax, sax in zip(axs,secaxs):
    print(pax.get_legend_handles_labels())
    print(sax.get_legend_handles_labels())
    handles, labels = [(a + b) for a, b in zip(pax.get_legend_handles_labels(),sax.get_legend_handles_labels() )]
    pax.legend(handles, labels,loc='upper center', 
             bbox_to_anchor=(0.5, 1.15),ncol=2)
#ax[1].legend(handles = [lplot1,rplot1] , labels=['A', 'B'],loc='upper center', 
#             bbox_to_anchor=(0.5, -0.2),fancybox=False, shadow=False, ncol=3)
#fig.autofmt_xdate()
#fig.suptitle('10-year German government bond yield & {}'.format(param), fontsize=16)

#l1 = inr["s"].plot(ax=axs[0],secondary_y=True, xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)
#l2 = inr["PX_Last"].plot(ax=axs[1], xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)
#l3 = inr["S_U"].plot(ax=axs[1], xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)

#print(axs[0].get_legend_handles_labels())

#plt.savefig('paper/bond/US_fig1.png')
#plt.savefig('paper/bond/US_fig1.eps')
#fig.tight_layout()
plt.savefig(prefix + "fig6.png",bbox_inches='tight')
plt.savefig(prefix + "fig6.eps",bbox_inches='tight')