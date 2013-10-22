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
import subprocess

class PhotoLogic():
    def queryName(self):
        if self.reverse: return ('', '')
        dlg = wx.TextEntryDialog(None, u"请输入您的学号", u"信息采集", '')
        dlg.ShowModal()
        if self.no_exit:
            while str(dlg.GetValue()).strip() == '':
                dlg.ShowModal()
        message = dlg.GetValue().strip()
        if not message: sys.exit(0)
        if os.path.isfile(os.path.join(self.baseraw, message + self.fmt)):
            message += '.' + str(random.randint(0,10000));
        dlg.Destroy()
        return (message, message)
            
    def querySkip(self):
        dlg = wx.SingleChoiceDialog(None, "", u"人员选择",
            [(n + ('(OK)' if os.path.isfile(os.path.join(
                 self.baseraw, f + self.fmt)) else ''))
                 for n, f in self.students], wx.CHOICEDLG_STYLE)
        dlg.SetSelection(self.at)
        if dlg.ShowModal() == wx.ID_OK:
            selected = dlg.GetSelection()
            dlg.Destroy()
            self.at = selected
            if self.remain == 0: self.remain = 1 
        dlg.Destroy()

    def __init__(self, csvfile='',
            basepath='', fmt='.jpg',
            baseraw='', baseprint='',
            printer='', reverseLogic=False):
        self.base = basepath
        self.baseraw = baseraw
        self.baseprint = baseprint
        self.printer = printer
        self.students = []
        self.at = 0
        self.remain = 0
        self.fmt = fmt
        self.current = ('', '')
        self.no_exit = False
        self.reverse = reverseLogic
        try:
            with open(csvfile, 'rb') as csvf:
                dialect = csv.Sniffer().sniff(
                        csvf.read(1024), delimiters=';,')
                csvf.seek(0); reader = csv.reader(csvf, dialect)
                self.students = [line for line in reader]
                for n, f in self.students:
                    if os.path.isfile(os.path.join(self.baseraw,
                        f + self.fmt)) == self.reverse:
                         self.remain += 1
                if os.path.isfile(os.path.join(self.baseraw,
                    self.students[0][1] + self.fmt)) != self.reverse:
                    self.nextStudent()
        except: pass

    def nextStudent(self):
        self.current = ('', '')
        if self.remain:
            cur = (self.at + 1) % len(self.students)
            while cur != self.at:
                if os.path.isfile(os.path.join(self.baseraw,
                    self.students[cur][1] + self.fmt)) == self.reverse:
                    self.at = cur
                    return 
                else:
                    cur =  (cur + 1) % len(self.students)
                    if cur == 0 and self.reverse:
                        self.remain = 0
                        return
            self.remain = 0 

    def name(self):
        if self.remain == 0 and (self.current == '' or self.current == ('', '')):
            self.current = self.queryName()
        if self.remain:
            return self.students[self.at][0]
        else: return self.current[0]

    def filename(self):
        if self.remain == 0 and (self.current == '' or self.current == ('', '')):
            self.current = self.queryName()
        if self.remain:
            return self.students[self.at][1]
        else: return self.current[1]

    def skip(self):
        if self.remain == 0: self.current = ('', '')
        else: self.querySkip()

    def save(self, img=None, raw=None, pr=None):
        if self.remain == 0:
            current = self.current
            self.current = ('', '')
        else:
            current = self.students[self.at]
            self.remain -= 1
            self.nextStudent()

        if img and self.base:
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

        if pr and self.baseprint:
            newimg = cv.CreateImageHeader(
                (pr.width, pr.height), cv.IPL_DEPTH_8U, 3)
            cv.SetData(newimg, numpy.zeros(
                (pr.height, pr.width, 3), numpy.uint8).tostring())
            cv.CvtColor(pr, newimg, cv.CV_BGR2RGB)
            filename = os.path.join(
                self.baseprint, current[1] + self.fmt)
            cv.SaveImage(filename, newimg)
            if sys.platform.startswith('win32') and self.printer:
                result = subprocess.check_output(
                        ["rundll32.exe",
                         "shimgvw.dll", "ImageView_PrintTo",
                         "/pt", filename, self.printer])
