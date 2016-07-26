# -*- coding: utf-8 -*-
"""
Transform zooniverse classification CSV file to BRAMS CSV file
Created on Jun 22 2016

@author: stijnc
"""

import json
import csv

DATE = date #20160714

zooniverse_classification_file = "input/radio-meteor-zoo-classifications-%s.csv" % DATE
output = {}
with open(zooniverse_classification_file) as csvfile:
     classifications = csv.DictReader(csvfile)
     for row in classifications:
         if row['workflow_version'] == "17.47":
             username = row['user_name']
             subject = json.loads(row['subject_data'])
             filename = subject[subject.keys()[0]]['Filename']
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
    output_filename = "input/csv/20160101_0000_BEUCCL_%s.csv" % username
    with open(output_filename, 'wb') as csvfile:
        fieldnames = ['filename','file_start','start (s)','end (s)','frequency_min (Hz)','frequency_max (Hz)',
                      'type',' top (px)',' left (px)',' bottom (px)',' right (px)','sample_rate (Hz)','fft',
                      'overlap','color_min','color_max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
        writer.writeheader()
        data.sort(key=lambda element: (element['filename'], element[' left (px)']))
        writer.writerows(data)