# -*- coding: utf-8 -*-
"""
Get percentage of completion of the active workflow
If this percentage is above a threshold, an email is automatically sent

Created on 18-July-2019
@author: stijnc
Copyright (C) 2019 Stijn Calders

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

from panoptes_client import Project
import argparse
import smtplib
from email.mime.text import MIMEText

def panoptes_get_workflow_completion():
    project = Project.find(slug='zooniverse/radio-meteor-zoo')
    
    wkfs = project.links.workflows
    for wkf in wkfs:
        if wkf.active:
            break
    return (wkf.display_name, 100*wkf.completeness)

def send_mail(message="", mail_from="radiometeorzoo@aeronomie.be", mail_to="stijn.calders@aeronomie.be"):
    msg = MIMEText(message)
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = message
    s = smtplib.SMTP('localhost')
    s.sendmail(mail_from, mail_to, msg.as_string())
    s.quit()
    
def main():
    parser = argparse.ArgumentParser(description='Get percentage of completion of the active workflow. If this percentage is above a threshold, an email is automatically sent')
    parser.add_argument("--threshold", type=float, default=0.95,
                        help="An email is automatically sent if completion is above this threshold")
    
    
    args = parser.parse_args()
    threshold = args.threshold

    display_name, completeness = panoptes_get_workflow_completion()
    
    if completeness >= threshold:
        text = "Workflow '{}' almost completed: {:2.0f}%".format(display_name, completeness)
        send_mail(text)

if __name__=="__main__":
    main()