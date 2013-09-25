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
import cv2, numpy
import threading
import settings

def rotateImage(image):
    shape = (image.width, image.height)
    image_center = (image.width / 2, image.width / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, 90, 1.)

    newimage = numpy.zeros((image.width, image.height, 3), numpy.uint8)
    newshape = (image.height, image.width);
    image = numpy.asarray(image[:,:])
    cv2.warpAffine(image, rot_mat, newshape,
            newimage, flags=cv2.INTER_LINEAR)
    
    bitmap = cv.CreateImageHeader(newshape, cv.IPL_DEPTH_8U, 3)
    cv.SetData(bitmap, newimage.tostring())
    return bitmap

class Camera:
    def __init__(self, which = 0):
        self.cap = cv.CaptureFromCAM(which)
        self.lock = threading.Lock()

    def getImage(self):
        self.lock.acquire()
        cv.GrabFrame(self.cap)
        img = cv.RetrieveFrame(self.cap)
        if img and settings.ROT: img = rotateImage(img)
        self.lock.release()
        return img
