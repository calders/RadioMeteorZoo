# -*- coding: utf-8 -*-
"""
Advanced user classification statistics
Created on Wed Aug 23 21:49:01 2017

@author: stijnc

Copyright (C) 2017 Stijn Calders

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact details:
________________________________________________
Stijn Calders
Space Physics - Space Weather

Royal Belgian Institute for Space Aeronomy (BIRA-IASB)
Ringlaan 3
B-1180 Brussels
BELGIUM

phone  : +32 (0)2 373.04.19
e-mail : stijn.calders@aeronomie.be
web    : www.aeronomie.be
________________________________________________
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

DATE = "20170821"

input_file = "input/radio-meteor-zoo-classifications-%s-statistics.csv" % DATE
#df = pd.read_csv(input_file, parse_dates=['first','last'], index_col=['username'])
#df2 = df[df.index.str.contains('not-logged-in')]
#df3 = df[~df.index.str.contains('not-logged-in')]
##series2 = pd.Series([1] * len(df2), index=df2['first'])
##series2 = series2.resample('1H').sum().cumsum()
##series2.plot(label="not logged in")
##series3 = pd.Series([1] * len(df3), index=df3['first'])
##series3 = series3.resample('1H').sum().cumsum()
##series3.plot(label="logged in")
##plt.xlabel("Date")
##plt.ylabel("# volunteers")
##plt.legend()
#
#df2.plot.hist('nbr_of_files',bins=100)
#df3.plot.hist('nbr_of_files',bins=100)
#
##first_date = df.min()['first']
##df['seniority'] = (df['last'] - df['first']).astype('timedelta64[h]')
##df['first'] = (df['first'] - first_date).astype('timedelta64[h]')
##df.drop('last', 1)
###print(df.head())
###pd.plotting.scatter_matrix(df, c=df.nbr_of_files)
##x=df['first']
##y=df['seniority']
##z=df['nbr_of_files']
##plt.scatter(x, y, c=z, norm=matplotlib.colors.LogNorm())
##plt.colorbar()
##plt.title("color=nbr of classified files")
##plt.xlabel("date of first classification")
##plt.ylabel("period between first and last classification")
##plt.show()
##

plt.style.use('ggplot')
df = pd.read_csv(input_file, parse_dates=['first','last'], index_col=['first'])
df2 = df[df.username.str.contains('not-logged-in')]
df4 = df2.resample('D').count().cumsum()
df4.username.plot()
plt.xlabel("")
plt.xticks(size=16)
plt.yticks(size=16)
plt.ylabel("")
plt.ylim(0,5500)
plt.title("")