# -*- coding: utf-8 -*-
"""
Draw rectangles on spectrogram
Created on Tue Aug 08 09:15:54 2017

@author: stijnc
"""

import utils

INPUT_FILES = {"20161210_0130": ["input/csv/not-logged-in-4fad9a359df7c642c960.csv "],
               "20161210_0155": ["input/csv/lwang752.csv"],
               "20161210_0215": ["input/csv/sdevnan.csv"],
               "20161210_0230": ["input/csv/Arabmoney3000.csv"],
               "20161210_0320": ["input/csv/airvolk.csv"],
               "20161210_0445": ["input/csv/not-logged-in-7452d1d2f47c73099a30.csv"],
               "20161210_0450": ["input/csv/not-logged-in-1681fe4d7a497e1751b3.csv"],
               "20161210_0505": ["input/csv/not-logged-in-7452d1d2f47c73099a30.csv"],
               "20161210_0530": ["input/csv/joyzheng8.csv"],
               "20161210_0540": ["input/csv/not-logged-in-672958733cffc2995843.csv"],
               "20161210_0600": ["input/csv/Arabmoney3000.csv"],
               "20161210_0625": ["input/csv/not-logged-in-e688e6955d346e4d3d36.csv"],
               "20161210_0650": ["input/csv/airvolk.csv"],
               "20161210_0710": ["input/csv/not-logged-in-4bc131f3a6089848f012.csv"]
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