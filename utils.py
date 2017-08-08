# -*- coding: utf-8 -*-
"""
BRAMS Radio Meteor Zoo utility functions
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

import csv
import numpy as np
from scipy.ndimage import measurements
from pylab import argwhere
import random
import sidereal #http://infohost.nmt.edu/tcc/help/lang/python/examples/sidereal/ims/sidereal.py

optimal_nbr_of_counters = {1: 1, #k: optimal_nbr_of_counters
                           2: 2,
                           3: 2,
                           4: 2,
                           5: 3,
                           6: 3,
                           7: 3,
                           8: 3,
                           9: 4,
                           10: 4,
                           11: 4,
                           12: 5,
                           13: 5,
                           14: 5,
                           15: 5,
                           16: 6,
                           17: 6,
                           18: 6,
                           19: 6,
                           20: 7,
                           21: 7,
                           22: 7,
                           23: 8,
                           24: 8,
                           25: 8,
                           26: 8,
                           27: 9,
                           28: 9,
                           29: 9,
                           30:10,
                           31:10,
                           32:10,
                           33:11,
                           34:11,
                           35:12}

MASKSIZE = (595, 864)

def read_detection_file(file_csv):
    """Read the CSV files from the manual detection
    A matrix with the same size as the image is created;
    the elements corresponding with a meteor are set to 1
    """
    filename = REFERENCE_DETECTION_FILE
    mask = {filename:np.zeros(MASKSIZE, dtype=int)}
    with open(file_csv, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            if line['filename'] != filename:
                filename = line['filename']
                mask[filename] = np.zeros(MASKSIZE, dtype=int)
            right = int(float(line[' right (px)']))
            bottom = int(float(line[' bottom (px)']))
            left = int(float(line[' left (px)']))
            top = int(float(line[' top (px)']))
            mask[filename][595-top:595-bottom+1, left:right+1] = 1
    return mask

def read_detection_file_from_memory(meteors):
    """Read the meteor identifications from the Zooniverse volunteers
    A matrix with the same size as the image is created;
    the elements corresponding with a meteor are set to 1
    This function reads only information about 1 specific spectrogram
    """
    mask = {spectrogram:np.zeros(MASKSIZE, dtype=int)}
    for meteor in meteors:
        right = meteor[' right (px)']
        bottom = meteor[' bottom (px)']
        left = meteor[' left (px)']
        top = meteor[' top (px)']
        mask[spectrogram][bottom:top, left:right] = 1
    if not np.all(mask[spectrogram]==0):
        return mask

def read_detection_file_per_spectrogram(file_csv,spectrogram):
    """Read the CSV files from the manual detection
    A matrix with the same size as the image is created;
    the elements corresponding with a meteor are set to 1
    This function reads only information about 1 specific spectrogram
    """
    mask = {spectrogram:np.zeros(MASKSIZE, dtype=int)}
    with open(file_csv, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            if line['filename'] != spectrogram:
                continue
            right = int(float(line[' right (px)']))
            bottom = int(float(line[' bottom (px)']))
            left = int(float(line[' left (px)']))
            top = int(float(line[' top (px)']))
            mask[spectrogram][bottom:top, left:right] = 1
    if not np.all(mask[spectrogram]==0):
        return mask

def calculate_threshold_image(masks, counters=None):
    """Merge the mask matrices from several observers to create one matrix
    with overlapping parts (meteor detected by several observers)
    """
    total_mask = {}
    for counter, mask in masks.iteritems():
        if counters is None or counter in counters:
            try:            
                for when, matrix in mask.iteritems():
                    if when in total_mask:
                        total_mask[when] += matrix.copy()
                    else:
                        total_mask[when] = matrix.copy()
            except AttributeError:
                continue
    return total_mask

def random_combination(iterable, nbr_of_samples):
    """Random selection from itertools.combinations(iterable, nbr_of_samples)"""
    pool = tuple(iterable)
    population_size = len(pool)
    indices = sorted(random.sample(xrange(population_size), nbr_of_samples))
    return [pool[i] for i in indices]

def detect_borders(detections, minimum_width=None):
    """Wrapper function to detect the borders of a rectangle"""
    borders = {}
    for file, detection in detections.iteritems():
        border = detect_border(detection, minimum_width)
        borders[file] = border
    return borders
    
def detect_border(detection, minimum_width=None):
    """Detect the borders of a rectangle using a bounding box algorithm"""
    lw, num = measurements.label(detection) #labels connected regions
    border = []
    for nbr in range(1, num+1):
        B = argwhere(lw == nbr) #take one of the labeled regions
        (xstart, ystart), (xstop, ystop) = B.min(0), B.max(0) #find min & max (x,y) value of this region
        if minimum_width == None or xstop-xstart >= minimum_width:
            border.append([xstart, ystart, xstop, ystop])
    return border

def is_intersection(rect_a, rect_b):
    """Detect if 2 rectangles are intersecting"""
    #rect_XYZ[0]=left
    #rect_XYZ[1]=bottom
    #rect_XYZ[2]=right
    #rect_XYZ[3]=top
    separate = rect_a[2] < rect_b[0] or \
               rect_a[0] > rect_b[2] or \
               rect_a[3] < rect_b[1] or \
               rect_a[1] > rect_b[3]
    return not separate

def classify_detections(border_thresholds,border_references):
    """Compare meteor observations with the reference. (Wrapper function)
       Classify in true positive, false positive and false negative"""
    true_positives = {} #both in reference and observation
    false_positives = {} #only in observation
    false_negatives = {} #only in reference
    for filename, border_threshold in border_thresholds.iteritems():
        border_reference = border_references[filename]
        true_positive, false_positive, false_negative = classify_detection(border_threshold,border_reference)
        true_positives[filename] = true_positive
        false_positives[filename] = false_positive
        false_negatives[filename] = false_negative
    return (true_positives, false_positives, false_negatives)

def classify_detection(border_threshold,border_reference):
    """Compare meteor observations with the reference. 
       Classify in true positive, false positive and false negative"""
    true_positive = []
    false_positive = list(border_threshold)
    false_negative = list(border_reference)
    bref_used = [False] * len(border_reference)
    for rectangle in border_threshold:
        for i in range(len(border_reference)):
           if not bref_used[i]:
               rectangle_ref = border_reference[i]
               if is_intersection(rectangle_ref,rectangle):
                    bref_used[i]=True
                    true_positive.append(rectangle_ref)
                    false_positive.remove(rectangle)
                    false_negative.remove(rectangle_ref)
                    break
    return (true_positive, false_positive, false_negative)

def total(stats):
    if isinstance(stats, dict):
        total_stat = 0
        for filename, stat in stats.iteritems():
            total_stat = total_stat + len(stat)
        return total_stat
    elif isinstance(stats, list):
        return len(stats)
    else:
        raise Exception('Stats is not a list nor a dictionary')


def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation
        source: http://stackoverflow.com/questions/8930370/where-can-i-find-mad-mean-absolute-deviation-in-scipy
    """
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))
    
def color_gradient ( val, beg_rgb=(1.0, 0.0, 0.0), end_rgb=(0.0, 1.0, 0.0), val_min = 0, val_max = 100):
    """ function returns an RGB value based on the input value
        0 = red / 50 = orange / 100 = green
        It is used to color bars in a plot
    """
    val_scale = (1.0 * val - val_min) / (val_max - val_min)
    red = max([min([beg_rgb[0] + 0.5 * val_scale * (end_rgb[0] - beg_rgb[0]),1]),0])
    green = max([min([beg_rgb[1] + val_scale * (end_rgb[1] - beg_rgb[1]),1]),0])
    blue = max([min([beg_rgb[2] + val_scale * (end_rgb[2] - beg_rgb[2]),1]),0])
    return ( red, green, blue )

def perdelta(start, end, delta):
    """ Generator function that gives datetimes between start & end in steps of delta
        source: http://stackoverflow.com/questions/10688006/generate-a-list-of-datetimes-between-an-interval
    """
    curr = start
    while curr < end:
        yield curr
        curr += delta

def toJD(dt):
    """ Calculate the Julian Date based on a datetime
    """
    JD = float(sidereal.JulianDate.fromDatetime(dt))
    return JD

