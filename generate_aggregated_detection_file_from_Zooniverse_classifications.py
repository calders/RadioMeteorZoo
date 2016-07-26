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

import json
import csv
import glob
import os
import utils
from datetime import datetime
import pickle


PNG_DIRECTORY = "input/png/"
CSV_DIRECTORY = "input/csv/"
OUTPUT_DIRECTORY = "output/aggregated/"
MASKSIZE = (595, 864)
DATE = date #20160714

### Read Zooniverse classification file ###

zooniverse_classification_file = "input/radio-meteor-zoo-classifications-%s.csv" % DATE
retired_subjects = set()

#Compile a list of retired subjects
with open(zooniverse_classification_file) as csvfile:
     classifications = csv.DictReader(csvfile)
     for row in classifications:
         if row['workflow_version'] == "17.47":
             subject = json.loads(row['subject_data'])
             if subject[subject.keys()[0]]['retired'] != None:
                 retired_subjects.add(subject[subject.keys()[0]]['Filename'])                 
retired_subjects.remove("RAD_BEDOUR_20160105_2020_BEUCCL_SYS001.png") # something very strange happened with this subject!
                                                                      # it was retired, but then shown again
                 
#Collect identifications from this list of retired subjects
with open(zooniverse_classification_file) as csvfile:
     classifications = csv.DictReader(csvfile)
     identifications = {} #e.g. identifications['A_M_P'][0]['RAD_BEDOUR_...'][' bottom (px)']
     for row in classifications:
         if row['workflow_version'] == "17.47":
             subject = json.loads(row['subject_data'])
             filename = subject[subject.keys()[0]]['Filename']
             if filename in retired_subjects: # consider only retired subjects!
                 username = row['user_name']
                 annotations = json.loads(row['annotations'])
                 metadata = json.loads(row['metadata'])
                 if 'seen_before' in metadata.keys() and metadata['seen_before'] == True:
                     continue
                 meteors = []
                 for rectangle in annotations[0]['value']:
                     x = rectangle['x']
                     y = rectangle['y']
                     width = rectangle['width']
                     height = rectangle['height']
                     if x == None or y == None or width == None or height == None: #strange that this happens!!!
                         continue
                     meteors.append({
                               ' top (px)': int(y+height),
                               ' left (px)': int(x),
                               ' bottom (px)': int(y),
                               ' right (px)': int(x+width),
                              })                              
                 if not filename in identifications.keys():
                     identifications[filename] = {username: meteors}
                 elif not username in identifications[filename].keys():
                     identifications[filename][username] = meteors
                 else:
                     identifications[filename][username].append(meteors)

### Generate aggregated BRAMS detection file ###

aggregated_identifications = {}
for spectrogram, content in identifications.iteritems():
    detection_files = {}
    for user, meteors in content.iteritems():
        tmp = read_detection_file_from_memory(meteors)
        if tmp is not None:        
            detection_files[user] = tmp
    threshold_image = calculate_threshold_image(detection_files)
    alpha = 4
    binary_image = threshold_image[threshold_image.keys()[0]].copy() 
    binary_image[binary_image < alpha] = 0
    binary_image[binary_image >= alpha] = 1
    border_threshold = detect_border(binary_image)
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

output_filename = "output/aggregated/20160101_0000_BEUCCL_aggregated-%s.csv" % DATE
with open(output_filename, 'wb') as csvfile:
    fieldnames = ['filename','file_start','start (s)','end (s)','frequency_min (Hz)','frequency_max (Hz)',
                      'type',' top (px)',' left (px)',' bottom (px)',' right (px)','sample_rate (Hz)','fft',
                      'overlap','color_min','color_max']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
    writer.writeheader()
    for spectrogram, data in aggregated_identifications.iteritems():
        data.sort(key=lambda element: (element['filename'], element[' left (px)']))
        writer.writerows(data)