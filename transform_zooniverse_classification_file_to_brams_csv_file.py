# -*- coding: utf-8 -*-
"""
Transform zooniverse classification CSV file to BRAMS CSV file
Created on Jun 22 2016

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
import re

DATE = "20160906"
pattern = re.compile("RAD_BEDOUR_2016081.*_BEOVER_SYS001.png") #RAD_BEDOUR_20160810_2300_BEHUMA_SYS001.png

#remove old files
for file in glob.glob("input/csv/*.csv"):
    os.remove(file)

zooniverse_classification_file = "input/radio-meteor-zoo-classifications-%s.csv" % DATE
output = {}
with open(zooniverse_classification_file) as csvfile:
     classifications = csv.DictReader(csvfile)
     for row in classifications:
         if row['workflow_version'] == "17.47":
             username = row['user_name']
             subject = json.loads(row['subject_data'])
             if 'Filename' in subject[subject.keys()[0]]:
                 filename = subject[subject.keys()[0]]['Filename']
             else:
                 filename = subject[subject.keys()[0]]['filename']                     
             if not pattern.match(filename):
                 continue
             annotations = json.loads(row['annotations'])
             metadata = json.loads(row['metadata'])
             if 'seen_before' in metadata.keys() and metadata['seen_before'] == True:
                 continue
             for rectangle in annotations[0]['value']:
                 x = rectangle['x']
                 y = rectangle['y']
                 width = rectangle['width']
                 height = rectangle['height']
                 if x == None or y == None or width == None or height == None: #strange that this happens!!!
                     continue
                 dict = {'filename':filename,
                         'file_start': 'unk',
                         'start (s)': 'unk',
                         'end (s)': 'unk',
                         'frequency_min (Hz)': 'unk',
                         'frequency_max (Hz)': 'unk',
                         'type': 'unk',
                         ' top (px)': int(y+height),
                         ' left (px)': int(x),
                         ' bottom (px)': int(y),
                         ' right (px)': int(x+width),
                         'sample_rate (Hz)': 'unk',
                         'fft': 'unk',
                         'overlap': 'unk',
                         'color_min': 'unk',
                         'color_max': 'unk'}
                 if not username in output.keys():
                     output[username] = [dict]
                 else:
                     output[username].append(dict)

for username, data in output.iteritems():
    output_filename = "input/csv/%s.csv" % username
    with open(output_filename, 'wb') as csvfile:
        fieldnames = ['filename','file_start','start (s)','end (s)','frequency_min (Hz)','frequency_max (Hz)',
                      'type',' top (px)',' left (px)',' bottom (px)',' right (px)','sample_rate (Hz)','fft',
                      'overlap','color_min','color_max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
        writer.writeheader()
        data.sort(key=lambda element: (element['filename'], element[' left (px)']))
        writer.writerows(data)