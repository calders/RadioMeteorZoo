# -*- coding: utf-8 -*-
"""
Find optimal parameters for the data quality algorithm
Created on Tue Oct 24 10:15:15 2017

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

import time
start_time = time.time()

import utils
import glob
from datetime import datetime, timedelta
import numpy as np
import csv

CSV_DIRECTORY = "input/csv/"
OUTPUT_DIRECTORY = "output/"
DATE = "20170620"
MINIMUM_WIDTH = 1
START = datetime(2016, 1, 3, 12)
END = datetime(2016, 1, 5)
#END = datetime(2016, 1, 5) #end day+1!!
STATION = "BEUCCL"
SHOWER = "Quadrantids2016"
REFERENCE_FILE = "c:\\Users\\stijnc\\Desktop\\Quadrantids 2016\\QUADRANTIDS_BEUCCL.csv"

def write_output(results, header=False):
    """Output cost as function of outlier threshold and complex threshold, per spectrogram"""
    # TO DO: implement this as a separate thread (using multithreading)
    output_filename = OUTPUT_DIRECTORY + "outlier_removal-parameter_study.csv"
    with open(output_filename, 'ab') as csvfile:
        fieldnames = ['spectrogram', 'outlier_threshold', 'cost']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
        if header:
            writer.writeheader()
        writer.writerows(results)

def calculate_distance(image1, image2):
    """Calculate the distance between two images (intersection / union)"""
    intersection = np.sum(image1 & image2)
    union = np.sum(image1 | image2)
    fraction = float(intersection) / float(union)
    return fraction

# generate list of all spectrogram names
spectrograms = []
for result in utils.perdelta(START, END, timedelta(minutes=5)):
     spectrograms.append("RAD_BEDOUR_"+datetime.strftime(result,"%Y%m%d_%H%M")+"_"+STATION+"_SYS001")

csv_files = glob.glob(CSV_DIRECTORY+"*.csv")
write_output([], header=True) #write only the header
for spectrogram in spectrograms:
    output = []
    # load reference classifications
    spectrogram = spectrogram
    dt = datetime.strptime(spectrogram[11:24], "%Y%m%d_%H%M")
    print "Loading reference classification "+str(dt)
    reference_classification = utils.read_detection_file_per_spectrogram(REFERENCE_FILE,spectrogram+".wav", swap_topbottom=True)
    if reference_classification is None:
        continue        
    print("--- %s seconds ---" % (time.time() - start_time))
    
    # load volunteers' classifications
    print "Loading volunteers' classifications "+str(dt)
    volunteer_classifications = {}
    for csv_file in csv_files:     #read detection files
        volunteer_classification = utils.read_detection_file_per_spectrogram(csv_file, spectrogram+".png")
        if volunteer_classification:
            volunteer_classifications[csv_file] = volunteer_classification
    print("--- %s seconds ---" % (time.time() - start_time))
    if volunteer_classifications is None:
        print "*****"
        continue
    
    # calculate aggregated dataset (including all volunteers)
    dt = datetime.strptime(spectrogram[11:24], "%Y%m%d_%H%M")
    print "Calculating aggregated dataset (including all spectrograms) ("+str(dt)+")"

    _, binary_image = utils.aggregate_rectangles(volunteer_classifications, spectrogram=spectrogram)
    
    # calculate distance between aggregated and reference classification
    fraction = calculate_distance(binary_image, reference_classification[spectrogram+".wav"])
    output.append({"spectrogram": spectrogram,
                    "outlier_threshold": -1,
                    "cost": fraction})
    print("--- %s seconds ---" % (time.time() - start_time))
    
    # try different thresholds
    for outlier_threshold in np.linspace(0.0, 1.0, num=11):
        print "Calculating for spectrogram "+spectrogram+" and outlier threshold "+str(outlier_threshold)
        volunteer_classifications_outliers_removed = {}
        # remove outliers        
        for volunteer, result in volunteer_classifications.iteritems():
            fraction2 = calculate_distance(binary_image, result[spectrogram+".png"])
            if fraction2 >= outlier_threshold:
                volunteer_classifications_outliers_removed[volunteer] = volunteer_classifications[volunteer]
                print volunteer+" added"
        
        # calculate aggregated dataset (excluding outlier classifications)
        if volunteer_classifications_outliers_removed:
            _, binary_image_outliers_removed = utils.aggregate_rectangles(volunteer_classifications_outliers_removed, spectrogram=spectrogram)
            
            # calculate distance between aggregated and reference classification
            fraction3 = calculate_distance(binary_image_outliers_removed, reference_classification[spectrogram+".wav"])
            output.append({"spectrogram": spectrogram,
                            "outlier_threshold": outlier_threshold,
                            "cost": fraction3})
    write_output(output)
    print("--- %s seconds ---" % (time.time() - start_time))