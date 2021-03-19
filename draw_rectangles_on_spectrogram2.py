# -*- coding: utf-8 -*-
"""
Draw rectangles on spectrogram (2)
Created on Fri Dec 08 12:57:33 2017

@author: stijnc
"""

import utils
from datetime import datetime, timedelta

fp = "output/aggregated/Perseids2020_BEHUMA_aggregated-20200825.csv"
start = datetime(2020, 8, 13)
end = datetime(2020, 8, 21) #end day+1!!

for result in utils.perdelta(start, end, timedelta(minutes=5)):
    dt = datetime.strftime(result,"%Y%m%d_%H%M")
    print(dt)
    try:
        spectrogram, rectangles = utils.read_rectangle_coordinates(fp, dt)
        output_filename = "%s.png" % (spectrogram[:-4])
        title = "%s" % (spectrogram)
        utils.plot_rectangles_on_spectrogram(spectrogram, 
                                             rectangles, # rectangles = array of [xstart, ystart, xstop, ystop]
                                             output_filename=output_filename, 
                                             title=title)
    except IndexError:
        continue
    except FileNotFoundError:
        continue