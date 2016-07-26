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

matplotlib.use('Agg')

DATE = date #20160714

def color_gradient ( val, beg_rgb, end_rgb, val_min = 0, val_max = 1):
    val_scale = (1.0 * val - val_min) / (val_max - val_min)
    return ( beg_rgb[0] + 0.5 * val_scale * (end_rgb[0] - beg_rgb[0]),
             beg_rgb[1] + val_scale * (end_rgb[1] - beg_rgb[1]),
             beg_rgb[2] + val_scale * (end_rgb[2] - beg_rgb[2]))

(datetime,identifications,volunteers) = pickle.load( open( "output/pickles/brams_zoo_meteor_identification-"+DATE+".p", "rb" ) )

df = pd.DataFrame({'counts': identifications, 'classifications': volunteers, 'spectrograms': 1}, index=datetime)
binned = df.resample('1H', how='sum')
binned.classifications_per_spectrogram = binned.classifications / binned.spectrograms
binned.percentage_completed = 100 * binned.classifications / (10 * binned.spectrograms)

fig = plt.figure()
fig.patch.set_facecolor('white')
ax1 = plt.subplot(2, 1, 1)
plt.plot(binned.index, binned.counts, marker='None', lw=2)
plt.gcf().autofmt_xdate()
plt.title("Radio Meteor Zoo\n (Quadrantids 2016, Uccle receiving station)",size=20,weight='bold')
plt.ylabel('Meteor activity',size=16,style='italic')
plt.yticks(size=14)
plt.ylim([0,1.2*max(binned.counts)])
plt.xlim([binned.index.min(), binned.index.max()])
plt.grid(axis='x')
ax1.xaxis.set_major_formatter(plt.NullFormatter())
ax1.fill_between(binned.index, 0, binned.counts, alpha=.3)
ax1.fill_between(binned.index, 0, binned.counts, alpha=.3)
ax1.spines["top"].set_visible(False)    
ax1.spines["right"].set_visible(False)

ax2 = plt.subplot(2, 1, 2)
ax2.spines["top"].set_visible(False)  
ax2.spines["right"].set_visible(False)  
grad_beg, grad_end = ( 1.0, 0.0, 0.0), (0.0, 1.0, 0.0)
col_list = [ color_gradient( val,
                             grad_beg,
                             grad_end,
                             0,
                             100) for val in binned.percentage_completed]
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
plt.savefig("output/plots/motivate_volunteers-%s.png" % DATE, figsize=(16,9), dpi=300)