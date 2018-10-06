#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 19:03:50 2018

@author: roccodeb
"""

# importing required modules
from zipfile import ZipFile
from Entity.Point import Point
from Entity.User import User
from Entity.Detection import Detection
import os
import re


def get_dataset():
    # specifying the zip file name
    file_name = "Geolife Trajectories 1.3.zip"
    userlist = []
    # opening the zip file in READ mode
    with ZipFile(file_name, 'r') as zipfile:
        # printing all the contents of the zip file
        for elem in zipfile.infolist():
            if not (elem.is_dir()):
                # print("Directory")
                # else:
                filepath, filename = os.path.split(elem.filename)
                filepath, trajectory = os.path.split(filepath)
                filepath, user = os.path.split(filepath)
                if filename.endswith(".plt") and not (filename.startswith("._")):
                    # print("\t"+user)
                    curuserinlist = None
                    for itemUser in userlist:
                        if itemUser.get_identifier() == user:
                            # esiste gia
                            curuserinlist = itemUser
                    if not curuserinlist:
                        curuserinlist = User(user)
                        userlist.append(curuserinlist)

                    curfile = zipfile.open(elem.filename)
                    # line 1.. 5 are useless in this dataset
                    for i in range(5):
                        curfile.readline()
                    line = curfile.readline()
                    curfilename = re.sub('\.plt$', '', filename)
                    pointlist = []
                    # count=0 #number of point
                    while line:
                        line = curfile.readline()
                        line = line.decode('UTF-8')
                        if line:
                            # count +=1
                            latitudine, longitudine, zero, altitudine, date, dates, times = line.split(",")
                            pointlist.append(Point(latitudine, longitudine, date))

                    # print("\tcount: {}".format(count))
                    # print("\t\t"+curFileName+"\n")

                    curuserinlist.add_detection(Detection(curfilename, pointlist))

                # elif filename.endswith("labels.txt"):
                # print("\t\tlables")
                # else:
                # print("not my file")
    zipfile.close()
