# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 12:38:54 2017

@author: stijnc
"""

FILE = "C:\\Users\\stijnc\\Documents\\GitHub\\RadioMeteorZoo\\output\\aggregated\\alphaMonocerotids2016_BEHUMA_aggregated-20171205.csv"

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


def parser(filename):
    #RAD_BEDOUR_20171121_0000_BEHUMA_SYS005.png
    _, _, date, time, _, _ = filename.split('_')
    output = dt.datetime.strptime(date+' '+time, '%Y%m%d %H%M')
    return output   

df = pd.read_csv(FILE, parse_dates=[0], date_parser=parser)
df2 = df.groupby(['filename']).count()
df2 = df2.loc[:,['file_start']]
df2.columns = ['Raw']
df3 = df2.rolling(12, center=True).mean()
df3.columns = ['Rolling average (1H)']
df4 = df2['Raw'] - df3['Rolling average (1H)']

#ax = df2.plot()
#ax.set_ylabel("Nbr of meteors")
#ax.set_xlabel("Time")
#ax.set_title(r'$\alpha\ Monocerotids$')
#df3.plot(ax=ax)
#plt.show()

ax = df4.plot(label="Raw - rolling avg")
ax.set_ylabel("Raw - rolling avg")
ax.set_xlabel("Time")
ax.set_title(r'$\alpha\ Monocerotids$')
ax.axhline(y=df4.mean()+3*df4.std(),c='red',label="AVG+3*STD")
ax.legend()
plt.show()