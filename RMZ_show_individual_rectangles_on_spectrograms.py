# -*- coding: utf-8 -*-
"""
Show individual results from Zooniverse volunteers on the spectrograms
Created on Tue 25 April 2017

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

import glob, csv, sys
import utils #RMZ utility functions
from datetime import datetime, timedelta
#Plotting libraries
import matplotlib.pyplot as plt
#import matplotlib.patches as patches
#from PIL import Image, ImageDraw
import cv2 as cv

plt.ioff() # Turn interactive plotting off

PNG_DIRECTORY = "X:\\projecten\\brams\\2019\\thesis Stan\\blind_test\\"
CSV_DIRECTORY = "X:\\projecten\\brams\\2019\\thesis Stan\\blind_test\\"
OUTPUT_DIRECTORY = "X:\\projecten\\brams\\2019\\thesis Stan\\blind_test\\"
start = datetime(2018, 10, 13)
end = datetime(2018, 12, 18)
station = "BEHUMA"

def renderBoundingBoxes(target, bboxes, rgb=(255, 0, 0)):
    r, g, b = rgb
    for bbox in bboxes:
        cv.rectangle(target, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (b, g, r), 1)

meteors = {}
for result in utils.perdelta(start, end, timedelta(minutes=5)):
    specgram_name = "RAD_BEDOUR_"+datetime.strftime(result,"%Y%m%d_%H%M")+"_"+station+"_SYS001.png"
    meteors[specgram_name] = list()

for csv_file in glob.glob(CSV_DIRECTORY+"*.csv"):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            spectrogram = line['filename']
            left = int(float(line[' left (px)'])) 
            right = int(float(line[' right (px)']))            
            bottom = int(float(line[' bottom (px)']))
            top = int(float(line[' top (px)']))
            if spectrogram in meteors.keys():
                meteors[spectrogram].append([left, bottom, right, top])
        
for spectrogram, meteor in meteors.items():
    if not meteor:
        continue
    try:
         img = cv.imread(PNG_DIRECTORY+spectrogram)
         renderBoundingBoxes(img, meteor)
         cv.imwrite(OUTPUT_DIRECTORY+spectrogram[:-4]+"_annotated.png", img)
    except IOError as e:
        print ("{0} ({1})".format(e.strerror,spectrogram))
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise