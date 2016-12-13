# -*- coding: utf-8 -*-
"""
Get user classification statistics
Created on Aug 17 2016

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

DATE = str(classification_date) #20160714

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
#             pattern = re.compile("RAD_BEDOUR_2016081.*_BEHUMA_SYS001.png") #RAD_BEDOUR_20160810_2300_BEHUMA_SYS001.png
#             if not pattern.match(filename):
#                 continue
             metadata = json.loads(row['metadata'])
             if 'seen_before' in metadata.keys() and metadata['seen_before'] == True:
                 continue
             if not username in output.keys():
                 output[username] = [filename]
             else:
                 output[username].append(filename)

output_filename = "input/radio-meteor-zoo-classifications-%s-statistics.csv" % DATE
with open(output_filename, 'wb') as csvfile:                 
    fieldnames = ['username','nbr_of_files']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
    writer.writeheader()
    for username, data in output.iteritems():
        writer.writerow({'username': username, 'nbr_of_files': len(data)})