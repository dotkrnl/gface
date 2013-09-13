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

import cv2.cv as cv
import threading

class Camera:
    def __init__(self, which = 0):
        self.cap = cv.CaptureFromCAM(which)
        self.lock = threading.Lock()
    
    def getImage(self):
        self.lock.acquire()
        cv.GrabFrame(self.cap)
        img = cv.RetrieveFrame(self.cap)
        self.lock.release()
        return img


    
