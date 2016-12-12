# -*- coding: utf-8 -*-
"""
Generate aggregated BRAMS detection file based on Zooniverse classifications
Created on Thu Jul 14 16:44:50 2016

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

import csv
import utils
import glob
from datetime import datetime, timedelta

CSV_DIRECTORY = "input/csv/"
OUTPUT_DIRECTORY = "output/aggregated"
DATE = "20161207"
minimum_width = 1
start = datetime(2016, 7, 22)
end = datetime(2016, 8, 20) #end day+1!!
STATION = "BEUCCL"
SHOWER = "Perseids"

spectrograms = []
for result in utils.perdelta(start, end, timedelta(minutes=5)):
     spectrograms.append("RAD_BEDOUR_"+datetime.strftime(result,"%Y%m%d_%H%M")+"_"+STATION+"_SYS001.png")

aggregated_identifications = {}
csv_files = glob.glob(CSV_DIRECTORY+"*.csv")
for spectrogram in spectrograms:
    dt = datetime.strptime(spectrogram[11:24], "%Y%m%d_%H%M")
    print dt
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
    if nbr_volunteers > 0:
        if nbr_volunteers <= 35:
            alpha = utils.optimal_nbr_of_counters[len(detection_files)]
        else:
            alpha = 12 #we don't know better...
        binary_image = threshold_image[threshold_image.keys()[0]].copy() 
        binary_image[binary_image < alpha] = 0
        binary_image[binary_image >= alpha] = 1
        border_threshold = utils.detect_border(binary_image,minimum_width=minimum_width)
        meteors = []
        for element in border_threshold:
            dict = {'filename': spectrogram,
                   'file_start': 'unk',
                   'start (s)': 'unk',
                   'end (s)': 'unk',
                   'frequency_min (Hz)': 'unk',
                   'frequency_max (Hz)': 'unk',
                   'type': 'unk',
                   ' top (px)': element[2],
                   ' left (px)': element[1],
                   ' bottom (px)': element[0],
                   ' right (px)': element[3],
                   'sample_rate (Hz)': 'unk',
                   'fft': 'unk',
                   'overlap': 'unk',
                   'color_min': 'unk',
                   'color_max': 'unk'}
            meteors.append(dict)
        aggregated_identifications[spectrogram] = meteors

### Output aggregated BRAMS detection file ###
output_filename = "output/aggregated/%s_%s_aggregated-%s.csv" % (SHOWER, STATION, DATE)
with open(output_filename, 'wb') as csvfile:
    fieldnames = ['filename','file_start','start (s)','end (s)','frequency_min (Hz)','frequency_max (Hz)',
                      'type',' top (px)',' left (px)',' bottom (px)',' right (px)','sample_rate (Hz)','fft',
                      'overlap','color_min','color_max']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
    writer.writeheader()
    for spectrogram, data in sorted(aggregated_identifications.iteritems()):
        data.sort(key=lambda element: element[' left (px)'])
        writer.writerows(data)