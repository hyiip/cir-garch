import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import time

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["figure.figsize"] = (8,6)
#inr = pd.read_csv("output/bondlowerUS/result/ust10yyield/day30SD2/roll/roll_lower_day30_SD200_ust10yyield.csv",index_col=0)
inr = pd.read_csv("output/bondlowerGER/result/F91010Y/day30SD8/roll/roll_lower_day30_SD800_F91010Y.csv",index_col=0)

print(inr)

# t = inr.index.values


# s1 = inr["s"].to_numpy() 
# s2 = inr[inr.columns[0]].to_numpy() 
# s3 = inr["S_U"].to_numpy() 
# t = [dt.datetime.strptime(date, "%d/%m/%Y") for date in t]
#print(t)
# plt.scatter(x, y)
# plt.show()

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
fig.subplots_adjust(hspace=0)

ax0 = axs[0].twinx()
inr["s"].plot(ax = ax0, linestyle="dashed", color = "red" ,label="x (right)", linewidth = 1)
print(ax0.get_legend_handles_labels())
axs[0].get_yaxis().set_visible(False)
inr[inr.columns[0]].plot(ax = axs[1] , label="10Y GER gov. bond Yield (left)", linewidth = 1)
inr["S_U"].plot(ax = axs[1] , linestyle="dotted", color="green", label="Upper Bound (left)", linewidth = 1)

handles, labels = [(a + b) for a, b in zip(ax0.get_legend_handles_labels(), axs[1].get_legend_handles_labels())]
axs[0].legend(handles, labels, loc='upper left',frameon=False)
ax0.set_ylabel('x')
axs[1].set_ylabel('10Y GER gov. bond Yield')
axs[1].set_ylim(bottom = 0)
ax0.set_ylim(bottom = 0)

fig.suptitle('10-year German government bond yield', fontsize=16)

#l1 = inr["s"].plot(ax=axs[0],secondary_y=True, xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)
#l2 = inr["PX_Last"].plot(ax=axs[1], xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)
#l3 = inr["S_U"].plot(ax=axs[1], xticks = (np.arange(0, len(inr)+1, 500.0)),legend=0)

#print(axs[0].get_legend_handles_labels())

#plt.savefig('paper/bond/US_fig1.png')
#plt.savefig('paper/bond/US_fig1.eps')
plt.savefig('paper/bond/GER_fig1.png')
plt.savefig('paper/bond/GER_fig1.eps')