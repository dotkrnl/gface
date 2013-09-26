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

import numpy
import cv2.cv as cv
import defaults
import face as faceUtil

def normalizeImage(img):
    cv.CvtColor(img, img, cv.CV_BGR2RGB)
    cv.Flip(img, img, 1)

def fakeFace(imgh, imgw):
    size = min(imgh, imgw)
    return ((imgw - size) / 2,
            (imgh - size) / 2,
            size, size)

def locateFace((imgh, imgw), (desth, destw),
        (fwx, fhx, fw, fh), media = defaults.SCREEN):
    hwradio = float(desth) / destw
    newheight = max(
        fh * media["mul"],
        fw * media["mul"] * hwradio
    )
    newwidth = max(
        fw * media["mul"],
        fh * media["mul"] / hwradio
    )

    if newheight > imgh or newwidth > imgw:
        newheight, newwidth = (
            min(imgh, imgw * hwradio),
            min(imgw, imgh / hwradio)
        )
    
    rhx, rhy, rwx, rwy = fhx, fhx + fh, fwx, fwx + fw
    rhx = int(rhx - (newheight - fh) * media["top"])
    rhy = int(rhy + (newheight - fh) * (1 - media["top"]))
    rwx = int(rwx - (newwidth - fw) * media["left"])
    rwy = int(rwy + (newwidth - fw) * (1 - media["left"]))

    if rhx < 1: rhy -= rhx - 1; rhx = 1
    if rwx < 1: rwy -= rwx - 1; rwx = 1
    if rhy > imgh: rhx -= rhy - imgh; rhy = imgh
    if rwy > imgw: rwx -= rwy - imgw; rwy = imgw
    return (rwx, rwy, rhx, rhy)


def getCrop(img, (w, h), face = None, media = defaults.SCREEN):
    if face == None:
        face = faceUtil.detectExec(img)
        if face == None:
            raise Exception("No face detected.")
    crop = locateFace((img.height, img.width), (h, w), face, media)
    return crop

def getFineImage(img, crop, (w, h)):
    old = img[crop[2]:crop[3], crop[0]:crop[1]]
    img = cv.CreateImage((w, h), img.depth, img.nChannels)
    cv.Resize(old, img)
    return img

def stepCrop(old, new, cur):
    def step(o, n, c): return int(float(o) + c*(float(n)-o))
    return (step(old[0], new[0], cur),
            step(old[1], new[1], cur),
            step(old[2], new[2], cur),
            step(old[3], new[3], cur))

def newImg(img):
    newimg = cv.CreateImageHeader(
        (img.width, img.height), cv.IPL_DEPTH_8U, 3)
    cv.SetData(newimg, numpy.zeros(
        (img.height, img.width, 3), numpy.uint8).tostring())
    return newimg
