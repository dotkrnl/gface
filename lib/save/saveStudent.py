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
import wx
import random

class PhotoSave():
    def queryName(self):
        dlg = wx.TextEntryDialog(None, u"请输入您的学号", u"信息采集", '')
        if dlg.ShowModal() == wx.ID_OK:
            message = dlg.GetValue()
            if os.path.isfile(os.path.join(self.base, message + self.fmt)):
                message += '.' + str(random.randint(0,10000));
            dlg.Destroy()
            return (message, message)
        else:
            dlg.Destroy()
            sys.exit(0)
            
    def __init__(self, csvfile, basepath, fmt, baseraw=''):
        self.base = basepath
        self.baseraw = baseraw
        self.students = []
        self.at = 0
        self.remain = 0
        self.fmt = fmt
        self.current = ''
        try:
            with open(csvfile, 'rb') as csvf:
                dialect = csv.Sniffer().sniff(
                        csvf.read(1024), delimiters=';,')
                csvf.seek(0); reader = csv.reader(csvf, dialect)
                self.students = [line for line in reader]
                for n, f in self.students:
                    if not os.path.isfile(os.path.join(self.base,
                        f + self.fmt)):
                         self.remain += 1
                if os.path.isfile(os.path.join(self.base,
                    self.students[0][1] + self.fmt)):
                    self.nextStudent()
        except: pass

    def nextStudent(self):
        if self.remain:
            cur = (self.at + 1) % len(self.students)
            while cur != self.at:
                if not os.path.isfile(os.path.join(
                    self.base, self.students[cur][1] + self.fmt)):
                    self.at = cur
                    return 
                else: cur =  (cur + 1) % len(self.students)
            self.remain = 0 

    def name(self):
        if self.remain == 0 and self.current == '':
            self.current = self.queryName()
        if self.remain:
            return self.students[self.at][0]
        else: return self.current[0]

    def querySkip(self):
        dlg = wx.SingleChoiceDialog(None, "", u"人员选择",
            [(n + ('(完成)' if os.path.isfile(os.path.join(
                 self.base, f + self.fmt)) else ''))
                 for n, f in self.students], wx.CHOICEDLG_STYLE)
        dlg.SetSelection(self.at)
        if dlg.ShowModal() == wx.ID_OK:
            selected = dlg.GetSelection()
            dlg.Destroy()
            self.at = selected
            if self.remain == 0: self.remain = 1 

    def skip(self):
        if self.remain == 0: self.current = ''
        else: self.querySkip()

    def save(self, img, raw=None):
        if self.remain == 0:
            current = self.current
            self.current = ''
        else:
            current = self.students[self.at]
            self.remain -= 1
            self.nextStudent()
        newimg = cv.CreateImageHeader(
                (img.width, img.height), cv.IPL_DEPTH_8U, 3)
        cv.SetData(newimg, numpy.zeros(
            (img.height, img.width, 3), numpy.uint8).tostring())
        cv.CvtColor(img, newimg, cv.CV_BGR2RGB)
        cv.SaveImage(os.path.join(
            self.base, current[1] + self.fmt), newimg)
        if raw and self.baseraw: 
            cv.SaveImage(os.path.join(
                self.baseraw, current[1] + self.fmt), raw)
