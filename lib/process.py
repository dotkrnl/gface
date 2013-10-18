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

import util
import copy
import sets
import math
import numpy
import cv2.cv as cv

def averageRBG(array):
    result = [0 for i in xrange(0, len(array[0]))]
    for i in xrange(0, 3):
        sum = 0
        for j in xrange(0, len(array)):
            sum += array[j][i]
        result[i] = sum / len(array)
    return tuple(result)

def distRBG(arr1, arr2):
    dist = 0
    for i in xrange(0, 3):
        #dist = max(dist, abs(arr2[i] - arr1[i]))
        dist = math.pow(arr2[i] - arr1[i], 2)
    return math.sqrt(dist)

#def change(img, i, j, h, w, middle, dest = (255., 255., 255., 0.), diff = 64.):
#    able = False
#    able = able or ((i == 0 or j == 0) or (i == h-1 or j == w-1))
#    able = able or ((i > 0 and j > 0) and cv.Get2D(img, i-1, j-1) == dest)
#    able = able or ((i > 0) and cv.Get2D(img, i-1, j) == dest)
#    able = able or ((j > 0) and cv.Get2D(img, i, j-1) == dest)
#    able = able or ((j < w-2) and cv.Get2D(img, i, j+1) == dest)
#    able = able and distRBG(cv.Get2D(img, i, j), middle) <= diff
#    if able: cv.Set2D(img, i, j, dest)

def floodFill(img, queue, h, w, middle, dest = (255., 255., 255., 0.), softdiff = 12., harddiff = 64.):
    visited = sets.Set(queue); need = []
    while queue:
        loc = queue.pop(0)
        need.append(loc)
        for mvx in xrange(-1, 1 + 1):
            for mvy in xrange(-1, 1 + 1):
                newLoc = (loc[0] + mvx, loc[1] + mvy)
                if newLoc in visited: continue
                if newLoc[0] < 0 or newLoc[0] >= h: continue
                if newLoc[1] < 0 or newLoc[1] >= w: continue
                oldColor = cv.Get2D(img, loc[0], loc[1])
                newColor = cv.Get2D(img, newLoc[0], newLoc[1])
                if (distRBG(oldColor, newColor) <= softdiff
                and distRBG(newColor, middle) <= harddiff):
                    queue.append(newLoc)
                    visited.add(newLoc)
    for (i, j) in need:
        cv.Set2D(img, i, j, dest)

def getPhoto(origin, media):
    img = util.getFineImage(origin,
        util.getCrop(origin, (media["width"], media["height"]), media = media),
        (media["width"], media["height"]))
    util.normalizeImage(img)
    try: media["background"]
    except: pass
    else:
        middle = averageRBG([cv.Get2D(img, 1, 1), cv.Get2D(img, 1, 2),
                             cv.Get2D(img, 2, 1), cv.Get2D(img, 2, 2)])
        queue = [(0, j) for j in xrange(0, img.width)]
        floodFill(img, queue, img.height, img.width,
            middle, media["background"]);
#        for i in xrange(0, img.height):
#            for j in xrange(0, img.width):
#                change(img, i, j, img.height, img.width,
#                       middle, media["background"])
#            for j in xrange(img.width-1, -1, -1):
#                change(img, i, j, img.height, img.width,
#                       middle, media["background"])"""
    return img

def getPrint(origin, media):
    img = cv.CreateImageHeader(
        (media["printer_w"], media["printer_h"]), cv.IPL_DEPTH_8U, 3)
    cv.SetData(img, numpy.zeros(
        (img.height, img.width, 3), numpy.uint8).tostring())
    cv.Set(img, (255, 255, 255))
    margin = media["margin"]
    singleheight = origin.height + 2 * margin
    singlewidth = origin.width + 2 * margin
    line = int(media["height"] / singleheight)
    col = int(media["width"] / singlewidth)
    for l in xrange(0, line):
        for c in xrange(0, col):
            cv.SetImageROI(img, 
                (c * singlewidth + margin, l * singleheight + margin, 
                origin.width, origin.height))
            cv.Copy(origin, img)
            cv.ResetImageROI(img)
    return img
