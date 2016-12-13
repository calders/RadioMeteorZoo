# -*- coding: utf-8 -*-
"""
Compare meteor activity measured by different stations
Created on Aug 29, 2016

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
import matplotlib
import numpy as np
from datetime import datetime

matplotlib.use('Agg')

DATE = "20160906"
show_radiant_altitude = True
lat = np.deg2rad(50.85)  # latitude of the receiving station [°]
lon = np.deg2rad(4.35)   # longitude of the receiving station [°]
rad_pos = {datetime(2016, 8, 10): [45,57], # radiant position (RA,Dec) for a given date
           datetime(2016, 8, 15): [51,58]}

def load_and_plot(ax, station, title):
    (dt,identifications,volunteers) = pickle.load( open( "output/pickles/brams_zoo_meteor_identification-"+str(DATE)+"-"+station+".p", "rb" ) )
    
    df = pd.DataFrame({'counts': identifications, 'classifications': volunteers, 'spectrograms': 1}, index=dt)
    binned = df.resample('1H', how='sum')
    binned.classifications_per_spectrogram = binned.classifications / binned.spectrograms
    binned.percentage_completed = 100 * binned.classifications / (10 * binned.spectrograms)
    
    plt.plot(binned.index, binned.counts, marker='None', lw=2)
    plt.gcf().autofmt_xdate()
    plt.title(title,size=18,weight='bold')
    plt.ylabel('Meteor activity',size=16,style='italic')
    plt.yticks(size=14)
    plt.ylim([0,1.2*max(binned.counts)])
    plt.xlim([binned.index.min(), binned.index.max()])
    plt.grid(axis='x')
    ax.fill_between(binned.index, 0, binned.counts, alpha=.3)
    ax.fill_between(binned.index, 0, binned.counts, alpha=.3)
    ax.spines["top"].set_visible(False)    
    ax.spines["right"].set_visible(False)

fig = plt.figure()
fig.suptitle("Comparison for 10 August",size=18,weight='bold')
fig.patch.set_facecolor('white')
ax = plt.subplot(2, 3, 1)
load_and_plot(ax, "BEHAAC", "Haacht")
ax = plt.subplot(2, 3, 2)
load_and_plot(ax, "BEOPHA", "Ophain")
ax = plt.subplot(2, 3, 3)
load_and_plot(ax, "BEHUMA", "Humain")
ax = plt.subplot(2, 3, 4)
load_and_plot(ax, "BEOTTI", "Ottignies")
ax = plt.subplot(2, 3, 5)
load_and_plot(ax, "BEMAAS", "Maasmechelen")
ax = plt.subplot(2, 3, 6)
load_and_plot(ax, "BEOVER", "Overpelt")