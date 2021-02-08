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

inr[inr.columns[0]].plot.hist(bins = 100)
plt.show()