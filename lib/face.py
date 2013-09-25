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

#### Copyright for trained XML file (./lib/subexec/*.xml) - 人工智能特征文件版权信息 ####

# Copyright (C) 2000, Intel Corporation, all rights reserved.
# Third party copyrights are property of their respective owners.
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#    * Redistribution's of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#    * Redistribution's in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#        and/or other materials provided with the distribution.
#    * The name of Intel Corporation may not be used to endorse or promote products
#        derived from this software without specific prior written permission.
# This software is provided by the copyright holders and contributors "as is" and
# any express or implied warranties, including, but not limited to, the implied
# warranties of merchantability and fitness for a particular purpose are disclaimed.
# In no event shall the Intel Corporation or contributors be liable for any direct,
# indirect, incidental, special, exemplary, or consequential damages
# (including, but not limited to, procurement of substitute goods or services;
#  loss of use, data, or profits; or business interruption) however caused
# and on any theory of liability, whether in contract, strict liability,
# or tort (including negligence or otherwise) arising in any way out of
# the use of this software, even if advised of the possibility of such damage.

import time
import sys, os
import threading
import subprocess
import cv2.cv as cv
import tempfile

libdir = os.path.join(
                      os.path.dirname(os.path.abspath(__file__)),
                      "subexec"
                      )

def detectExec(img, tempname = None):
    if tempname == None:
        tempname = tempfile.mktemp(".jpg")
    try:
        cv.SaveImage(tempname, img)
        if sys.platform.startswith('win32'): useshell = True
        else: useshell = False
        result = subprocess.check_output(
                [os.path.join(libdir, 'getFace.py'),
                 tempname], shell = useshell)
        resultXY = result[:result.find('\n')]
        resultHW = result[result.find('\n') + 1:]
        return (
                int(resultXY[:resultXY.find(' ')]),
                int(resultXY[resultXY.find(' ') + 1:]),
                int(resultHW[:resultHW.find(' ')]),
                int(resultHW[resultHW.find(' ') + 1:])
                )
    except subprocess.CalledProcessError:
        return None
    finally:
        os.unlink(tempname)

class FaceThread(threading.Thread):
    def __init__(self, camera):
        threading.Thread.__init__(self)
        self.daemon = True
        self.cam = camera
        self.face = None
        self.fail = 0

    def run(self):
        while True:
            img = self.cam.getImage()
            if img:
                face = detectExec(img)
                if not face:
                    self.fail += 1
                    if self.fail > 5:
                        self.fail = 5
                        self.face = None
                if face:
                    self.fail = 0
                    self.face = face
            time.sleep(0.2)
