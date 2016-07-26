# -*- coding: utf-8 -*-
"""
Radio Meteor Zoo simulations - meteor based comparison between reference and observers
Display misses and false detections on spectrograms
Created on July 11 2016

@author: stijnc
"""

import csv
import glob
import utils
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime

PNG_DIRECTORY = "input/png/"
CSV_DIRECTORY = "input/csv/"
REFERENCE_DETECTION_FILE = "input/reference/QUADRANTIDS_BEUCCL.csv"
OUTPUT_DIRECTORY = "output/comparison/"
MASKSIZE = (595, 864)

#Step 1: read reference file
reference_detections = read_detection_file(REFERENCE_DETECTION_FILE)

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
        #plot missed meteors and false detections on spectrograms
        #red  = false detection
        #orange = missed
        if len(false_positives) > 0:
            false_positives_mask = np.zeros(MASKSIZE, dtype=int)
            for meteor in false_positives:
                bottom = meteor[0]            
                left = meteor[1]
                top = meteor[2]
                right = meteor[3]
                false_positives_mask[bottom:top+1, left:right+1] = 1
            plt.contour(false_positives_mask,colors='red')
        if len(false_negatives) > 0:
            false_negatives_mask = np.zeros(MASKSIZE, dtype=int)
            for meteor in false_negatives:
                bottom = meteor[0]            
                left = meteor[1]
                top = meteor[2]
                right = meteor[3]
                false_negatives_mask[bottom:top+1, left:right+1] = 1
            plt.contour(false_negatives_mask,colors='orange')
        if len(false_positives) > 0 or len(false_negatives) > 0:
            im = Image.open(PNG_DIRECTORY+spectrogram)
            
            plt.imshow(im,zorder=0)
            plt.title(spectrogram)
            plt.savefig(OUTPUT_DIRECTORY+spectrogram)
            plt.cla()