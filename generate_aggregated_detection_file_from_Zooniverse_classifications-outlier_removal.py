# -*- coding: utf-8 -*-
"""
Generate aggregated BRAMS detection file based on Zooniverse classifications
Outliers are removed in a second iteration
Created on 8 August 2017

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

import csv
import utils
import glob
from datetime import datetime, timedelta
import numpy as np

CSV_DIRECTORY = "input/csv/"
OUTPUT_DIRECTORY = "output/aggregated"
DATE = "20170620"
MINIMUM_WIDTH = 1
START = datetime(2016, 12, 10)
END = datetime(2016, 12, 11) #end day+1!!
STATION = "BEOTTI"
SHOWER = "Geminids2016"
OUTLIER_THRESHOLD = 0.10 #less than 10% overlap
COMPLEX_THRESHOLD = 0.20 #more than 20% of the volunteers are outliers

def write_output(aggregated_identifications, shower=SHOWER, station=STATION, date=DATE, run=1):
    """Output aggregated BRAMS detection file"""
    output_filename = "output/aggregated/%s_%s_aggregated-%s-run%d.csv" % (shower, station, date, run)
    with open(output_filename, 'wb') as csvfile:
        fieldnames = ['filename','file_start','start (s)','end (s)','frequency_min (Hz)','frequency_max (Hz)',
                          'type',' top (px)',' left (px)',' bottom (px)',' right (px)','sample_rate (Hz)','fft',
                          'overlap','color_min','color_max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
        writer.writeheader()
        for spectrogram, data in sorted(aggregated_identifications.iteritems()):
            data.sort(key=lambda element: element[' left (px)'])
            writer.writerows(data)

spectrograms = []
for result in utils.perdelta(START, END, timedelta(minutes=5)):
     spectrograms.append("RAD_BEDOUR_"+datetime.strftime(result,"%Y%m%d_%H%M")+"_"+STATION+"_SYS001.png")

aggregated_identifications = {"1st_run": {},
                              "2nd_run": {}}
csv_files = glob.glob(CSV_DIRECTORY+"*.csv")
for spectrogram in spectrograms:
    dt = datetime.strptime(spectrogram[11:24], "%Y%m%d_%H%M")
    print dt

    #read detection file
    detection_files = {}
    for csv_file in csv_files:
        tmp = utils.read_detection_file_per_spectrogram(csv_file,spectrogram)
        if tmp is not None:        
            detection_files[csv_file] = tmp
    #run meteor identification algorithm & select regions that are above identification threshold
    nbr_volunteers = len(detection_files)
    meteors, binary_image = utils.aggregate_rectangles(detection_files, spectrogram=spectrogram)
    aggregated_identifications["1st_run"][spectrogram] = meteors
    #compare volunteers with the aggregated result
    to_be_removed = []
    for volunteer, result in detection_files.iteritems():
        name = volunteer.split('\\')[1]
        intersection = np.sum(binary_image & result[result.keys()[0]])
        union = np.sum(binary_image | result[result.keys()[0]])
        fraction = float(intersection)/float(union)
        if fraction < OUTLIER_THRESHOLD:
            print "Volunteer %s removed" % name
            to_be_removed.append('input/csv\\'+name)
    if float(len(to_be_removed)) > COMPLEX_THRESHOLD * float(nbr_volunteers):
        print "Spectrogram %s is complex (%d out of %d removed)" % (spectrogram, len(to_be_removed), nbr_volunteers)
    else:
        #run meteor identification algorithm again (without outliers)
        for volunteer in to_be_removed:
            del detection_files[volunteer]
            meteors, _ = utils.aggregate_rectangles(detection_files, spectrogram=spectrogram)
            aggregated_identifications["2nd_run"][spectrogram] = meteors
write_output(aggregated_identifications["1st_run"],run=1)
write_output(aggregated_identifications["2nd_run"],run=2)