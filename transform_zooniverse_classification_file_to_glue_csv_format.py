# -*- coding: utf-8 -*-
"""
Transform zooniverse classification CSV file to Glue CSV file
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
from astropy.table import Table
from astropy.time import Time

zooniverse_classification_file = "input/radio-meteor-zoo-classifications.csv"
output = []
with open(zooniverse_classification_file) as csvfile:
     classifications = csv.DictReader(csvfile)
     for row in classifications:
         if row['workflow_version'] == "17.47":
             username = row['user_name']
             created_at = datetime.strptime(row['created_at'], "%Y-%m-%d %H:%M:%S UTC")
             subject = json.loads(row['subject_data'])
             filename = subject[subject.keys()[0]]['Filename']
             annotations = json.loads(row['annotations'])
             metadata = json.loads(row['metadata'])
             if 'seen_before' in metadata.keys() and metadata['seen_before'] == True:
                 continue
             nbr_rectangles = len(annotations[0]['value'])
             dt = datetime.strptime(filename[11:24], "%Y%m%d_%H%M")
             dict = {'username': username,
                     'created at': Time(created_at).decimalyear,
                     'filename': filename,
                     'datetime': Time(dt).decimalyear,
                     'nbr rectangles': nbr_rectangles}
             output.append(dict)


output_filename = "input/glue.csv"
#with open(output_filename, 'wb') as csvfile:
#    fieldnames = ['username','filename','datetime','top (px)','left (px)','bottom (px)','right (px)']
#    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)    
#    writer.writeheader()
#    for data in output:
#        print data
#        print fieldnames
#        writer.writerows(data)
with open(output_filename, 'wb') as csvfile:
    t = Table(rows=output)
    t.write(csvfile,format='ascii.csv')