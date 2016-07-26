# -*- coding: utf-8 -*-
"""
Download classifications file
Created on Mon Jul 12 15:34:53 2016

@author: stijnc
"""

filename = "panoptes_test2_export.csv"

from panoptes_client import Project, Panoptes
from panoptes_client.panoptes import PanoptesAPIException
import requests, sys

Panoptes.connect(username=username, password=password)

project = Project.find(slug='zooniverse/radio-meteor-zoo')

#r = project.get_classifications_export(generate=True, wait=True, wait_timeout=1800)
wait_timeout = 60
project.generate_classifications_export()
for attempt in range(60):
    print "wait classification export (attempt %d)" % attempt
    sys.stdout.flush()
    try:
        export = project.wait_classifications_export(wait_timeout)
    except PanoptesAPIException as e:
        print str(e)[:32]
        if str(e)[:32] == "classifications_export not ready":        
            continue
        else:
            raise
    except TypeError:
        print "TypeError!"
        continue # I don't know why this happens: TypeError: 'NoneType' object has no attribute '__getitem__' 
                 #                                (panoptes_clien\project.py, line 54)
    except:
        raise
    else:
        r = requests.get(export['media'][0]['src'],stream=True)
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(1024):
                fd.write(chunk)
        break
else:
    raise Exception('Failed to download classification file')