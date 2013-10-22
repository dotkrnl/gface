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

# Define inbuilt media type

SCREEN = {
    "top": 0.5,
    "left": 0.5,
    "mul": 2.1
}

PHOTO_BASE = {
    "NATIONAL_STUDENT": {
        "name": u"全国教务系统",
        "top": 0.65,
        "left": 0.5,
        "mul": 1.4,
        "width": 260,
        "height": 320,
        #"background":
        #   (199, 233, 245, 0),
    },
    "ONE_INCH": {
        "name": u"一寸",
        "top": 0.5,
        "left": 0.5,
        "mul": 1.6,
        "width": 318,
        "height": 449,
        #"background":
        #    (255, 0, 0, 0),
    },
    "TWO_INCH": {
        "name": u"两寸",
        "top": 0.4,
        "left": 0.5,
        "mul": 1.6,
        "width": 461,
        "height": 626,
    },
    "SMALL_TWO_INCH": {
        "name": u"小两寸",
        "top": 0.4,
        "left": 0.5,
        "mul": 1.6,
        "width": 390,
        "height": 567,
    },
    "ID_CARD": {
        "name": u"身份证照",
        "top": 0.5,
        "left": 0.5,
        "mul": 1.6,
        "width": 260,
        "height": 390,
    },
}

PRINT_BASE = {
    "THREE_R": {
        "name": u"3R",
        "height": 1500,
        "width": 1050,
        "printer_w": 1050,
        "printer_h": 1500,
        "margin": 10
    },
    "FOUR_R": {
        "name": u"4R",
        "height": 1800,
        "width": 1200,
        "printer_w": 1200,
        "printer_h": 1800,
        "margin": 15
    },
    "FIVE_R": {
        "name": u"5R",
        "height": 2100,
        "width": 1500,
        "printer_w": 1500,
        "printer_h": 2100,
        "margin": 17
    },
    "SIX_R": {
        "name": u"6R",
        "height": 2400,
        "width": 1800,
        "printer_w": 1800,
        "printer_h": 2400,
        "margin": 20
    },
    "EIGHT_R": {
        "name": u"8R",
        "height": 3000,
        "width": 2400,
        "printer_w": 2400,
        "printer_h": 3000,
        "margin": 20
    },
}
