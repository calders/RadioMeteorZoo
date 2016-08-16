# -*- coding: utf-8 -*-
"""
Create a subject set and upload new subjects to it
Created on Mon Jul 11 15:34:53 2016

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

from panoptes_client import SubjectSet, Subject, Project, Panoptes
#from panoptes_client.panoptes import PanoptesAPIException
import glob
import os
import time
import sys

print "[PYTHON] Create a subject set and upload new subjects to it"

start_time = time.time()

if os.environ.has_key("ZOO_USERNAME"):
  username = os.environ["ZOO_USERNAME"]
if os.environ.has_key("ZOO_PASSWORD"):
  password = os.environ["ZOO_PASSWORD"]
if os.environ.has_key("ZOO_SUBJECTSET"):
  subject_set_display_name = os.environ["ZOO_SUBJECTSET"]
if os.environ.has_key("BRAMS_STATION"):
  station = os.environ["BRAMS_STATION"]
station = "BEHUMA_13"
#if os.environ.has_key("DATE"):
#  date = os.environ["DATE"]

Panoptes.connect(username=username, password=password)

project = Project.find(slug='zooniverse/radio-meteor-zoo')
#Update subjects
subjects = []
files = glob.glob('/data/incoming/brams/ZOO/'+station+'/*.png')
if len(files) == 0:
  raise Exception('Error finding PNG files. Did you specify correct station? (/data/incoming/brams/ZOO/'+station+'/*.png)')
metadata = open('/data/incoming/brams/'+station+'.zoo','r')
(fft,overlap,color_min,color_max) = metadata.readlines()

#Create uploaded directory if necessary
dest = '/data/incoming/brams/ZOO/'+station+'/uploaded/'
if not(os.path.isdir(dest)):
    os.mkdir(dest)

for file in files:
    print "Uploading file %s" % file
    sys.stdout.flush()
    subject = Subject()
    subject.links.project = project
    subject.add_location(file)
    # You can set whatever metadata you want, or none at all
    subject.metadata['filename'] = os.path.basename(file)
    #TODO subject.metadata['file_start'] = 
    #TODO subject.metadata['sample_rate'] = 5512
    subject.metadata['fft'] = fft 
    subject.metadata['overlap'] = overlap
    subject.metadata['color_min'] = color_min
    subject.metadata['color_max'] = color_max
    #TODO subject.metadata['width'] =
    #TODO subject.metadata['height'] =    
    subject.save()
    subjects.append(subject)
    os.rename(file,dest+os.path.basename(file)) #move file to uploaded directory
#Create a new subject set or append the subjects to an existing one
for subject_set in project.links.subject_sets:
    if str(subject_set.display_name) == subject_set_display_name:
        subject_set_id = subject_set.id
        subject_set = SubjectSet.find(subject_set_id)
        break
else:
    #subject_set = SubjectSet()
    #subject_set.links.project = project
    #subject_set.display_name = subject_set_display_name 
    #subject_set.save()
    raise Exception('Subject set does not exist')
subject_set.add(subjects) # SubjectSet.add_subjects() can take a list of Subjects, or just one.

print("--- %s seconds ---" % (time.time() - start_time))
