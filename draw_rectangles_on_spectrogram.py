# -*- coding: utf-8 -*-
"""
Draw rectangles on spectrogram
Created on Tue Aug 08 09:15:54 2017

@author: stijnc
"""

import utils

INPUT_FILES = {"20161210_0130": ["input/csv/not-logged-in-b0a850b9d522d96faa82.csv"],
               "20161210_0155": ["input/csv/lwang752.csv"],
               "20161210_0215": ["input/csv/sdevnan.csv"],
               "20161210_0230": ["input/csv/Arabmoney3000.csv"],
               "20161210_0320": ["input/csv/airvolk.csv"],
               "20161210_0445": ["input/csv/not-logged-in-1dbfa300448b6dccffe7.csv"],
               "20161210_0450": ["input/csv/not-logged-in-ae80753362a4a90a819a.csv"],
               "20161210_0505": ["input/csv/not-logged-in-1dbfa300448b6dccffe7.csv"],
               "20161210_0530": ["input/csv/joyzheng8.csv"],
               "20161210_0540": ["input/csv/not-logged-in-c6e6fcd021551140a57c.csv"],
               "20161210_0600": ["input/csv/Arabmoney3000.csv"],
               "20161210_0625": ["input/csv/not-logged-in-534b670e40a598857c12.csv"],
               "20161210_0650": ["input/csv/airvolk.csv"],
               "20161210_0710": ["input/csv/not-logged-in-3d2c0b879cea54123233.csv"]
              }
STANDARD_FILES = ["output/aggregated/Geminids2016_BEOTTI_aggregated-20170620-run1.csv",
                  "output/aggregated/Geminids2016_BEOTTI_aggregated-20170620-run2.csv"]

input_files = {dt: files + STANDARD_FILES for dt, files in INPUT_FILES.iteritems()}

for dt, files in input_files.iteritems():
    for fp in files:
        print dt, fp
        spectrogram, rectangles = utils.read_rectangle_coordinates(fp, dt)
        title = "%s \n %s" % (spectrogram, fp.split('/')[-1])
        if "run1" in fp:
            suffix = "run1"
        elif "run2" in fp:
            suffix = "run2"
        else:
            suffix = fp.split('/')[-1][:-4]
        output_filename = "%s-%s.png" % (spectrogram[:-4],suffix)
        utils.plot_rectangles_on_spectrogram(spectrogram, 
                                             rectangles, # rectangles = array of [xstart, ystart, xstop, ystop]
                                             output_filename=output_filename, 
                                             title=title) 