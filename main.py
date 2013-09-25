#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

#### Copyright for this software - 本软件的版权信息 ####

# Copyright (C) 2013 Jason Lau (刘家昌)
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

__author__ = "Jason Lau <i@dotkrnl.com>"
__copyright__ = "Copyright (C) 2013 Quanzhou No.1 Middle School"
__license__ = "Apache License"
__version__ = "1.0"

import wx
import time
import threading
import cv2.cv as cv
import lib.util as util
import lib.camera as cam
import lib.face as face
import lib.process as process
import lib.defaults as defaults
import lib.settings as settings
import lib.save as psave

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, u'人像采集系统')
        self.SetClientSize((800, 600))
        self.cam = cam.Camera()
        self.det = face.FaceThread(self.cam)
        self.det.start()
        self.oldCrop = self.oldSize = None
        self.curStatus = "camera"
        self.curOrigin = self.curDisplay = None
        self.saver = psave.PhotoSave(settings.FILE, settings.PHOTO)
        self.Bind(wx.EVT_IDLE, self.onIdle)
        self.Bind(wx.EVT_LEFT_DOWN, self.onConfirm)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onCancel)
    
    def displayImage(self, img, text=None):
        if not text: text = '请确认：' + self.saver.name()
        bitmap = wx.BitmapFromBuffer(img.width, img.height, img.tostring())
        offseth = (self.GetSize()[1] - img.height) / 2
        offsetw = (self.GetSize()[0] - img.width) / 2
        dc = wx.ClientDC(self)
        time.sleep(0.05) # avoid blue display
        dc.DrawBitmap(bitmap, offsetw, offseth, False)
        dc.SetFont(wx.Font(36, wx.SWISS, wx.NORMAL, wx.BOLD))
        dc.DrawText(text, 40, self.GetSize()[1]-100)
    
    def onCamera(self):
        img = self.cam.getImage()
        if img:
            crop = util.getCrop(img, self.GetSize(),
                                self.det.face or util.fakeFace(img.height, img.width))
            if (self.GetSize() == self.oldSize and
                    self.oldCrop and self.oldCrop != crop):
                for step in xrange(0, 3):
                    curCrop = util.stepCrop(self.oldCrop, crop, (step / 3.))
                    dis = util.getFineImage(self.cam.getImage() or img,
                                            curCrop, self.GetSize())
                    util.normalizeImage(dis)
                    self.displayImage(dis)
            self.curOrigin = self.cam.getImage() or img
            self.curDisplay = util.getFineImage(self.curOrigin, crop, self.GetSize())
            util.normalizeImage(self.curDisplay)
            self.displayImage(self.curDisplay)
            self.oldCrop = crop
            self.oldSize = self.GetSize()
    
    def onShot(self):
        if self.curDisplay:
            if self.doneShot:
                self.displayImage(self.curDisplay)
                return
            for times in xrange(0, 3):
                cv.AddS(self.curDisplay, (100, 100, 100), self.curDisplay)
                self.displayImage(self.curDisplay)
            try:
                self.curDisplay = process.getPhoto(self.curOrigin, settings.USE)
                self.displayImage(self.curDisplay)
            except Exception as e:
                self.curStatus = 'camera'
                print e
            self.doneShot = True
        else:
            self.curStatus = 'camera'

    def onIdle(self, event):
        if self.curStatus == 'camera':
            self.onCamera()
        if self.curStatus == 'shot':
            self.onShot()
        event.RequestMore()

    def onConfirm(self, event):
        if self.curStatus == 'camera':
            self.doneShot = False
            self.curStatus = 'shot'
        else:
            self.saver.save(self.curDisplay)
            self.curStatus = 'camera'

    def onCancel(self, event):
        if self.curStatus == 'camera':
            self.saver.skip()
        else:
            self.curStatus = 'camera'

if __name__=="__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show(True)
    app.MainLoop()
