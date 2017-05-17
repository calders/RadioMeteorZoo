# -*- coding: utf-8 -*-
"""
Show results from Zooniverse volunteers on the spectrograms
Created on Tue 16 August 2016

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

import glob
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import utils

plt.ioff() # Turn interactive plotting off

PNG_DIRECTORY = "input/png/"
CSV_DIRECTORY = "input/csv/"
OUTPUT_DIRECTORY = "output/"
MASKSIZE = (595, 864)
start = datetime(2016, 8, 19)
end = datetime(2016, 8, 20)
station = "BEHUMA"

spectrograms = []
for result in utils.perdelta(start, end, timedelta(minutes=5)):
     spectrograms.append("RAD_BEDOUR_"+datetime.strftime(result,"%Y%m%d_%H%M")+"_"+station+"_SYS001.png")

csv_files = glob.glob(CSV_DIRECTORY+"*.csv")
date_time, identifications, volunteers = [], [], []
for spectrogram in spectrograms:
    dt = datetime.strptime(spectrogram[11:24], "%Y%m%d_%H%M")
    #Step 1: read detection file
    detection_files = {}
    for csv_file in csv_files:
        tmp = utils.read_detection_file_per_spectrogram(csv_file,spectrogram)
        if tmp is not None:        
            detection_files[csv_file] = tmp
    #Step 2: run meteor identification algorithm
    threshold_image = utils.calculate_threshold_image(detection_files)
    #Step 3: select regions that are above identification threshold
    nbr_volunteers = len(detection_files)
    if nbr_volunteers > 0: # and nbr_volunteers <= 10:
        alpha = utils.optimal_nbr_of_counters[len(detection_files)]
        binary_image = threshold_image[threshold_image.keys()[0]].copy() 
        binary_image[binary_image < alpha] = 0
        binary_image[binary_image >= alpha] = 1
        border_thresholds = utils.detect_border(binary_image)
        #Step 4: plot these regions on spectrograms
        im = Image.open(PNG_DIRECTORY+spectrogram)
        fig,ax = plt.subplots(1)
        ax.imshow(im,zorder=0)
        for [xstart, ystart, xstop, ystop] in border_thresholds:
            ax.add_patch(patches.Rectangle((xstart, ystart), xstop - xstart, ystop - ystart, edgecolor="red", fill=False))
        plt.title(spectrogram+" ("+str(nbr_volunteers)+" volunteers)")
        plt.savefig(OUTPUT_DIRECTORY+spectrogram)                        
        plt.cla()