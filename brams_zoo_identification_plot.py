# -*- coding: utf-8 -*-
"""
Create meteor activity graph to motivate participants of the Radio Meteor Zoo
Created on Wed Jun 22 19:19:10 2016

@author: stijnc

Copyright (C) 2016 Stijn Calders

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

import matplotlib.pyplot as plt
import pandas as pd
import pickle
import matplotlib.dates as md
import matplotlib
import sidereal #http://infohost.nmt.edu/tcc/help/lang/python/examples/sidereal/ims/sidereal.py
import numpy as np
from scipy import interpolate
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

matplotlib.use('Agg')

DATE = "20161124"
STATION = "BEOVER"
title = "Radio Meteor Zoo\n (Perseids 2016, Overpelt receiving station)"
show_radiant_altitude = True
lat = np.deg2rad(50.85)  # latitude of the receiving station [°]
lon = np.deg2rad(4.35)   # longitude of the receiving station [°]
rad_pos = {datetime(2016, 8, 10): [45,57], # radiant position (RA,Dec) for a given date
           datetime(2016, 8, 15): [51,58]}
#rad_pos = {datetime(2015, 12, 31): [228,50], # radiant position (RA,Dec) for a given date
#           datetime(2016, 1, 5): [231,49],
#           datetime(2016, 1, 10): [234,48]}
OUTPUT_PLOT = "Perseids2016-%s-%s.png" % (DATE, STATION)

(dt,identifications,volunteers) = pickle.load( open( "output/pickles/brams_zoo_meteor_identification-"+DATE+"-"+STATION+".p", "rb" ) )

df = pd.DataFrame({'counts': identifications, 'classifications': volunteers, 'spectrograms': 1}, index=dt)
binned = df.resample('1H', how='sum')
binned.classifications_per_spectrogram = binned.classifications / binned.spectrograms
binned.percentage_completed = 100 * binned.classifications / (10 * binned.spectrograms)

fig = plt.figure()
fig.patch.set_facecolor('white')
ax1 = plt.subplot(2, 1, 1)
plt.plot(binned.index, binned.counts, marker='None', lw=2)
plt.gcf().autofmt_xdate()
plt.title(title,size=18,weight='bold')
plt.ylabel('Meteor activity\n(Min. duration: 10s)',size=16,style='italic',color='blue')
plt.yticks(size=14)
plt.ylim([0,1.2*max(binned.counts)])
plt.xlim([binned.index.min(), binned.index.max()])
plt.grid(axis='x')
ax1.xaxis.set_major_formatter(plt.NullFormatter())
ax1.fill_between(binned.index, 0, binned.counts, alpha=.3)
ax1.fill_between(binned.index, 0, binned.counts, alpha=.3)
ax1.spines["top"].set_visible(False)    
ax1.spines["right"].set_visible(False)

# Plot radiant altitude
if show_radiant_altitude:
    JDs = map(toJD,rad_pos.keys())
    pos = np.deg2rad(rad_pos.values()).tolist()
    retrieve = interpolate.interp1d(JDs, pos, axis=0)
    ax1b = ax1.twinx()
    for utc in perdelta(min(dt), max(dt), timedelta(minutes=60)):
        RA, Dec = retrieve(toJD(utc))
        equ_coord = sidereal.RADec(RA,Dec)
        h = equ_coord.hourAngle(utc,lon)
        horiz_coord = equ_coord.altAz(h,lat)
        ax1b.set_ylabel('Radiant elevation [$\degree$]',size=16,style='italic',color='green')
        ax1b.scatter(utc,np.rad2deg(horiz_coord.alt),marker='.',color='green')
ax1.autoscale(True,axis='x',tight=True)

ax2 = plt.subplot(2, 1, 2)
ax2.spines["top"].set_visible(False)  
ax2.spines["right"].set_visible(False)  
col_list = [ color_gradient(val) for val in binned.percentage_completed]
plt.bar(binned.index, height=binned.percentage_completed, width=1/24., color = col_list)
locs, labels = plt.xticks()
plt.setp(labels, rotation=45)
plt.xticks(size=14)
plt.grid(axis='x')
xfmt = md.DateFormatter('%d %b')
ax2.xaxis.set_major_formatter(xfmt)
plt.yticks(size=14)
plt.ylim(0, 100)
plt.ylabel("Classification\ncompleteness (%)",size=16,style='italic')
plt.savefig("output/plots/%s.png" % OUTPUT_PLOT, figsize=(16,9), dpi=300)