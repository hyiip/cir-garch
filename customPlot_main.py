import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import time

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["figure.figsize"] = (8,5)

parameter = {
    "GER": {
        "title": "(Panel A)\n10-year German government bond yield",
        "upper": "Upper Bound, η_U = 3",
        "main": "10Y GER Gov. Bond Yield",
        "rawfile": "paper/bond/roll_lower_day30_SD800_F91010Y.csv",
        "savepng": "paper/bond/fig1_GER.png",
        "saveeps": "paper/bond/fig1_GER.eps"
        },
    "US": {
        "title": "(Panel B)\n10-year US Treasury yield",
        "upper": "Upper Bound, η_U = 1.5",
        "main": "10Y US Treasury Yield",
        "rawfile": "paper/bond/roll_lower_day30_SD200_ust10yyield.csv",
        "savepng": "paper/bond/fig1_US.png",
        "saveeps": "paper/bond/fig1_US.eps"
        }
    }
current = "US"
inr = pd.read_csv(parameter[current]["rawfile"],index_col=0)
#inr = pd.read_csv("output/bondlowerGER/result/F91010Y/day30SD8/roll/roll_lower_day30_SD800_F91010Y.csv",index_col=0)

print(inr)

# t = inr.index.values


# s1 = inr["s"].to_numpy() 
# s2 = inr[inr.columns[0]].to_numpy() 
# s3 = inr["S_U"].to_numpy() 
# t = [dt.datetime.strptime(date, "%d/%m/%Y") for date in t]
#print(t)
# plt.scatter(x, y)
# plt.show()


fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True,constrained_layout  = True)
fig.subplots_adjust(hspace=0)

ax0 = axs[0].twinx()
inr["s"].plot(ax = ax0, linestyle="dashed", color = "red" ,label="x (right)", linewidth = 1)
print(ax0.get_legend_handles_labels())
axs[0].get_yaxis().set_visible(False)
inr[inr.columns[0]].plot(ax = axs[1] , label="{} (left)".format(parameter[current]["main"]), linewidth = 1)
inr["S_U"].plot(ax = axs[1] , linestyle="dotted", color="green", label="{} (left)".format(parameter[current]["upper"]), linewidth = 1)

handles, labels = [(b + a) for a, b in zip(ax0.get_legend_handles_labels(), axs[1].get_legend_handles_labels())]
axs[0].legend(handles, labels, loc='upper left',frameon=False)
ax0.set_ylabel('x')
axs[1].set_ylabel(parameter[current]["main"])
axs[1].set_ylim(bottom = 0)
ax0.set_ylim(bottom = 0)

fig.autofmt_xdate()
fig.suptitle(parameter[current]["title"], fontsize=16)
#fig.suptitle('10-year German government bond yield', fontsize=16)

#l1 = inr["s"].plot(ax=axs[0],secondary_y=True, xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)
#l2 = inr["PX_Last"].plot(ax=axs[1], xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)
#l3 = inr["S_U"].plot(ax=axs[1], xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)

#print(axs[0].get_legend_handles_labels())

#plt.savefig('paper/bond/US_fig1.png')
#plt.savefig('paper/bond/US_fig1.eps')
#fig.tight_layout()
plt.savefig(parameter[current]["savepng"])
plt.savefig(parameter[current]["saveeps"])