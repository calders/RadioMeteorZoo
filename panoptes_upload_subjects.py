# -*- coding: utf-8 -*-
"""
Create a subject set and upload new subjects to it
Created on Mon Jul 11 15:34:53 2016

@author: stijnc
"""

from panoptes_client import SubjectSet, Subject, Project, Panoptes
#from panoptes_client.panoptes import PanoptesAPIException
import glob
import os
import time

start_time = time.time()

subject_set_display_name = 'My new subject set314'

Panoptes.connect(username=username, password=password)

project = Project.find(slug='stijnc/untitled-project-2015-07-08t13-16-53-dot-409z')
#Update subjects
subjects = []
for file in glob.glob('input/png/tmp/*.png'):
    print "Uploading file %s" % file
    subject = Subject()
    subject.links.project = project
    subject.add_location(file)
    # You can set whatever metadata you want, or none at all
    # filename, file_start, sample_rate (Hz), fft, overlap, color_min, color_max
    subject.metadata['filename'] = os.path.basename(file)
    #TODO subject.metadata['file_start'] = 
    subject.metadata['sample_rate'] = 5512
    subject.metadata['fft'] = 16384
    subject.metadata['overlap'] = 90
    #TODO subject.metadata['color_min'] =
    #TODO subject.metadata['color_max'] =
    for attempt in range(10):  
        try:
            subject.save()
        except:
            continue
        else:
            break
    subjects.append(subject)
#Create a new subject set or append the subjects to an existing one
for subject_set in project.links.subject_sets:
    if str(subject_set.display_name) == subject_set_display_name:
        subject_set_id = subject_set.id
        subject_set = SubjectSet.find(subject_set_id)
        break
else:
    subject_set = SubjectSet()
    subject_set.links.project = project
    subject_set.display_name = subject_set_display_name 
    subject_set.save()
subject_set.add_subjects(subjects) # SubjectSet.add_subjects() can take a list of Subjects, or just one.

print("--- %s seconds ---" % (time.time() - start_time))
