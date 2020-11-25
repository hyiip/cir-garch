import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import time

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["figure.figsize"] = (12,8)
plt.rcParams.update({'font.size': 16})
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

fig, axs = plt.subplots(constrained_layout=True)
fig.subplots_adjust(hspace=0)

param = "Leakage Ratio"
region = "GER"
prefix = "paper/bond/"
setting = {
    "GER": {
        "rawfile": prefix + "roll_lower_day30_SD800_F91010Y_no_max.csv",
        "outputprefix": prefix + "fig5_",
        "title": "Germany Gov. Bond Yield"
    },
    "US": {
        "rawfile": prefix + "roll_lower_day30_SD200_ust10yyield.csv",
        "outputprefix": prefix + "fig4_",
        "title": "US Treasury Yield"
    }
    }
variable = {
    "Leakage Ratio":{
        "panel": "D",
        "greek": r'$\sigma^2 / 4 \kappa \theta$',
        "label": "Leakage Ratio",
        "loc": "upper center",
        "nbins": 10,
        "png": "leakage.png",
        "eps": "leakage.eps"
    }
}
inr = pd.read_csv(setting[region]["rawfile"],index_col=0)
print(inr)
inr = inr.iloc[749:]
secax = axs.twinx()
axs.get_yaxis()

inr[inr.columns[0]].plot(
    ax = axs , label="{} (left)".format(setting[region]["title"]), linewidth = 1,
    xticks = np.arange(0, len(inr)+1, 250.0), 
    title= "Panel {}\n{} - {}".format(variable[param]["panel"],variable[param]["greek"],setting[region]["title"]))
inr["S_U"].plot(ax = axs, linestyle="dotted", color = "green" ,label="Uper Bound (left)", linewidth = 1)
inr["Leakage Ratio"].plot(
    ax = secax , label="{} (right)".format(variable[param]["greek"]), linestyle="dashed", color = "red",  linewidth = 1)

#axs.set_xticks(np.arange(0, len(inr)+1, 250.0))
print(secax.get_legend_handles_labels())
handles, labels = [(a + b) for a, b in zip(axs.get_legend_handles_labels(),secax.get_legend_handles_labels() )]
axs.legend(handles, labels, loc=variable[param]["loc"],frameon=False)
#axs.legend(handles, labels, loc=(0.01,0.12),frameon=False) #theta
#axs.legend(handles, labels, loc=(0.01,0.8),frameon=False) #sigma
#secax.set_ylabel('yield')
secax.set_ylabel(variable[param]["label"])
axs.set_ylabel("Yield")
#axs.set_ylim(0.375,0.43)
#axs.set_ylim(bottom = 0)
secax.set_ylim(bottom = 0, top = 1)
secax.locator_params(nbins=variable[param]["nbins"], axis='y')
fig.tight_layout()
fig.autofmt_xdate()
#fig.suptitle('10-year German government bond yield & {}'.format(param), fontsize=16)

#l1 = inr["s"].plot(ax=axs[0],secondary_y=True, xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)
#l2 = inr["PX_Last"].plot(ax=axs[1], xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)
#l3 = inr["S_U"].plot(ax=axs[1], xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)

#print(axs[0].get_legend_handles_labels())

#plt.savefig('paper/bond/US_fig1.png')
#plt.savefig('paper/bond/US_fig1.eps')
plt.savefig(setting[region]["outputprefix"] + variable[param]["png"],bbox_inches='tight')
plt.savefig(setting[region]["outputprefix"] + variable[param]["eps"],bbox_inches='tight')