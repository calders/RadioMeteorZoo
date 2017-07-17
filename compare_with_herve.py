# -*- coding: utf-8 -*-
"""
Find the 9 other users that have processed the same spectrograms as Hervé
Created on Tue Jul 11 15:17:08 2017

@author: stijnc
"""

INPUT_FILE = "input/radio-meteor-zoo-classifications-20170620.csv"
OUTPUT_FILE = "output/compare_with_herve.csv"

import pandas
import json
import csv

def get_filename(subject_data):
    filenames = []
    for subject_data_json in subject_data:
        subject = json.loads(subject_data_json)
        if 'Filename' in subject[subject.keys()[0]]:
             filename = subject[subject.keys()[0]]['Filename']
        else:
             filename = subject[subject.keys()[0]]['filename']
        filenames.append(filename)
    return filenames

def meteors(annotations):
    meteors = []
    for annotation_json in annotations:
        annotation = json.loads(annotation_json)
        try:
            raw_meteors = annotation[0]['value']
            for meteor in raw_meteors:
                meteors.append({'x': int(meteor['x']),
                                'y': int(meteor['y']),
                                'width': int(meteor['width']),
                                'height': int(meteor['height'])})
        except IndexError:
            meteors = None
    return meteors
    
df = pandas.read_csv(INPUT_FILE,usecols=['user_name','subject_data','annotations','workflow_version'])
df = df[df.workflow_version == 17.47]
df['filename'] = get_filename(df['subject_data'])
df.drop(['subject_data','workflow_version'], axis=1, inplace=True)

df2 = df[df['user_name'] == 'lams9999']
files = df2['filename']

with open(OUTPUT_FILE, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['file', 'user_name','x','y','width','height'])
    for filename in files:
        df3 = df[df['filename'] == filename]
        for user in df3.user_name:
            df4 = df3[df3['user_name'] == user]
            meteor_list = meteors(df4['annotations'])
            try:
                for meteor in meteor_list:
                    writer.writerow([filename,user,meteor['x'],meteor['y'],meteor['width'],meteor['height']])
            except IndexError:
                writer.writerow([filename,user,'None'])