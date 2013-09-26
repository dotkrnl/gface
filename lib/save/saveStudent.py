#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

# Copyright 2013 Jason Lau (刘家昌)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys
import csv
import cv2.cv as cv
import numpy

class PhotoSave():
    def __init__(self, csvfile, basepath, fmt):
        self.base = basepath
        self.students = []
        self.skips = []
        self.fmt = fmt
        try:
            with open(csvfile, 'rb') as csvf:
                dialect = csv.Sniffer().sniff(
                        csvf.read(1024), delimiters=';,')
                csvf.seek(0); reader = csv.reader(csvf, dialect)
                self.students = [line for line in reader
                        if not os.path.isfile(
                            os.path.join(self.base,
                            line[1] + self.fmt))]
                self.students.reverse()
        except int: print "err"

    def name(self):
        if len(self.students) == 0: return '完成'
        return self.students[len(self.students) - 1][0]

    def nextLoop(self):
        self.skips.reverse()
        self.students = self.skips
        self.skips = []

    def skip(self):
        if len(self.students) == 0: return
        self.skips.append(self.students.pop())
        if len(self.students) == 0: self.nextLoop()

    def save(self, img):
        if len(self.students) == 0: return
        current = self.students.pop()
        if len(self.students) == 0: self.nextLoop()
        newimg = cv.CreateImageHeader(
                (img.width, img.height), cv.IPL_DEPTH_8U, 3)
        cv.SetData(newimg, numpy.zeros(
            (img.height, img.width, 3), numpy.uint8).tostring())
        cv.CvtColor(img, newimg, cv.CV_BGR2RGB)
        cv.SaveImage(os.path.join(
            self.base, current[1] + self.fmt), newimg)
