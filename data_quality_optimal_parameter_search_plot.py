# -*- coding: utf-8 -*-
"""
Find optimal parameters for the data quality algorithm -- plot results
Created on Fri Nov 10 14:44:38 2017

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

FILE = "output/outlier_removal-parameter_study.csv"
df = pd.read_csv(FILE)
gp = df.groupby(['outlier_threshold'])
means = gp.mean()
errors = gp.std()
count = gp.count()

fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
ax1, ax2 = axs[0], axs[1]
plt1 = ax1.errorbar(x=means.index, y=means.cost, yerr=errors.cost, fmt='o', label='agreement with ground truth')
plt2 = ax2.scatter(x=means.index, y=count.cost, label='number of spectrograms', color='red')
fig.suptitle('RMZ outlier removal -- parameter study')
ax2.set_xlabel('Threshold')
ax1.set_ylabel('Agreement with ground truth')
ax2.set_ylabel('# spectrograms')
#plt.legend()
plt.show()