import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

inr = result = pd.read_csv("vixir/updating/extracted/VIX.csv", index_col=0)
normal = result = pd.read_csv("vix/updating/extracted/VIX.csv", index_col=0)

print(inr)
print(normal)

all = pd.concat([normal,inr],axis = 1)
all.columns = ["VIX","1/VIX"]
figsize=(16, 8)
fontsize = 16
ax1 = all.plot(title = "VIX comparsion", grid=True, fontsize=fontsize, secondary_y="1/VIX", figsize=(16, 8), xticks = (np.arange(0, len(all)+1, 250.0)))

ax1.right_ax.set_ylabel("1/VIX", fontsize = fontsize)
ax1.set_ylabel("VIX", fontsize = fontsize)
ax1.set_xlabel("Date", fontsize = fontsize)
ax1.title.set_fontsize(fontsize)
for item in (ax1.get_legend().get_texts()):
    item.set_fontsize(fontsize)
plt.autoscale(enable=True, axis='x', tight=True)
fig1 = ax1.get_figure()
fig1.autofmt_xdate()
fig1.savefig("output/VIX_comparsion.png" )
plt.close('all')
print(all)