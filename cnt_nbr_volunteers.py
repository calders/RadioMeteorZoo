# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 18:55:05 2019

@author: stijnc
"""

import pandas

df = pandas.read_csv("output/aggregated/Perseids2019_BEHUMA_aggregated-20190925.csv")
for i in range(20):
    print(i,':',len(df[df.nbr_volunteers==i])/len(df))
    