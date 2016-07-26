# -*- coding: utf-8 -*-
"""
Radio Meteor Zoo simulations - meteor based comparison between reference and observers
Created on July 7 2016

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
import glob
import numpy as np
import utils
import os
from datetime import datetime
import csv

PNG_DIRECTORY = "input/png/"
CSV_DIRECTORY = "input/csv/"
REFERENCE_FILE = "input/reference/QUADRANTIDS_BEUCCL.csv"
OUTPUT_DIRECTORY = "output/comparison/"
MASKSIZE = (595, 864)

csvout = csv.writer(open(OUTPUT_DIRECTORY + "comparison_with_reference.csv","wb"),dialect="excel")
csvout.writerow(['spectrogram, # volunteers, true_positives, false_positives, false_negatives, hits, misses, false_detections'])
summary = []

#Step 1: read reference file
reference_detections = read_detection_file(REFERENCE_FILE)

#Step 2: detect borders of reference detection file
border_references = detect_borders(reference_detections)

spectrograms = map(os.path.basename,glob.glob(PNG_DIRECTORY+"*.png"))
csv_files = glob.glob(CSV_DIRECTORY+"*.csv")
optimal_nbr_of_counters = {1: 1, #k: optimal_nbr_of_counters
                           2: 2,
                           3: 2,
                           4: 2,
                           5: 3,
                           6: 3,
                           7: 3,
                           8: 3,
                           9: 4,
                           10: 4}
for spectrogram in spectrograms:
    dt = datetime.strptime(spectrogram[11:24], "%Y%m%d_%H%M")
    #Step 3: read detection file
    detection_files = {}
    for csv_file in csv_files:
        tmp = read_detection_file_per_spectrogram(csv_file,spectrogram)
        if tmp is not None:        
            detection_files[csv_file] = tmp
    #Step 4: run meteor identification algorithm
    threshold_image = calculate_threshold_image(detection_files)
    
    #Step 5: select regions that are above identification threshold
    nbr_volunteers = len(detection_files)
    if nbr_volunteers > 0 and nbr_volunteers <= 10:
        alpha = optimal_nbr_of_counters[len(detection_files)]
        binary_image = threshold_image[threshold_image.keys()[0]].copy() 
        binary_image[binary_image < alpha] = 0
        binary_image[binary_image >= alpha] = 1
        border_threshold = detect_border(binary_image)
        key = spectrogram[:-4]+".wav"
        if key in border_references:
            border_reference = border_references[spectrogram[:-4]+".wav"]
        else:
            border_reference = []
        true_positives, false_positives, false_negatives = classify_detection(border_threshold,border_reference)
        if total(true_positives) == 0 and total(false_positives) == 0 and total(false_negatives) == 0:
            hits = 100.0
            misses = 0.0
            false_detections = 0.0
        else:
            try:        
                hits = 100.0 * float(total(true_positives)) / float(total(true_positives) + total(false_negatives))
                misses = 100.0 * float(total(false_negatives)) / float(total(true_positives) + total(false_negatives))
            except ZeroDivisionError:
                hits = 0
                misses = 0
            false_detections = 100.0 * float(total(false_positives)) / float(total(true_positives) + total(false_positives))
        csvout.writerow(([spectrogram, nbr_volunteers, total(true_positives), total(false_positives), total(false_negatives), int(hits), int(misses), int(false_detections)]))
    else:
        print "[warning] spectrogram %s has %d volunteers" % (spectrogram,nbr_volunteers)
