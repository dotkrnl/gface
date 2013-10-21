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
    "top": 0.3,
    "left": 0.5,
    "mul": 2.5
}

PHOTO_BASE = {
    "NATIONAL_STUDENT": {
        "name": "全国教务系统",
        "top": 0.65,
        "left": 0.5,
        "mul": 1.4,
        "width": 260,
        "height": 320,
        #"background":
        #   (199, 233, 245, 0),
    },
    "ONE_INCH": {
        "name": "一寸",
        "top": 0.5,
        "left": 0.5,
        "mul": 1.6,
        "width": 318,
        "height": 449,
        #"background":
        #    (255, 0, 0, 0),
    },
    "TWO_INCH": {
        "name": "两寸",
        "top": 0.5,
        "left": 0.5,
        "mul": 1.6,
        "width": 413,
        "height": 626,
    },
    "SMALL_TWO_INCH": {
        "name": "小两寸",
        "top": 0.5,
        "left": 0.5,
        "mul": 1.6,
        "width": 390,
        "height": 567,
    },
    "ID_CARD": {
        "name": "身份证照",
        "top": 0.5,
        "left": 0.5,
        "mul": 1.6,
        "width": 260,
        "height": 390,
    },
}

PRINT_BASE = {
    "THREE_R": {
        "name": "三寸",
        "height": 1500,
        "width": 1050,
        "printer_w": 2480,
        "printer_h": 3508,
        "margin": 10
    },
    "FOUR_R": {
        "name": "四寸",
        "height": 1800,
        "width": 1200,
        "printer_w": 2480,
        "printer_h": 3508,
        "margin": 15
    },
    "FIVE_R": {
        "name": "五寸",
        "height": 2100,
        "width": 1500,
        "printer_w": 2480,
        "printer_h": 3508,
        "margin": 17
    },
    "SIX_R": {
        "name": "六寸",
        "height": 2400,
        "width": 1800,
        "printer_w": 2480,
        "printer_h": 3508,
        "margin": 20
    },
    "EIGHT_R": {
        "name": "八寸",
        "height": 3000,
        "width": 2400,
        "printer_w": 2480,
        "printer_h": 3508,
        "margin": 20
    },
}
