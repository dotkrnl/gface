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

import os
import defaults
import logic.defaultLogic

FMT = '.jpg'
USE = defaults.PHOTO_BASE["TWO_INCH"]
USES = [ defaults.PHOTO_BASE["ONE_INCH"],
         defaults.PHOTO_BASE["TWO_INCH"],
         defaults.PHOTO_BASE["SMALL_TWO_INCH"],
         defaults.PHOTO_BASE["ID_CARD"],
         defaults.PHOTO_BASE["NATIONAL_STUDENT"]]
PHOTO = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../photo"
        )

PRINT_USES = [ defaults.PRINT_BASE["THREE_R"],
               defaults.PRINT_BASE["FOUR_R"],
               defaults.PRINT_BASE["FIVE_R"],
               defaults.PRINT_BASE["SIX_R"],
               defaults.PRINT_BASE["EIGHT_R"] ]
PRINT = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../print"
        )

PRINTER = "printer_name"

RAW = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../raw"
        )

ROT = False#True

SAVE = logic.defaultLogic.PhotoLogic 
FILE = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../students.csv"
        )

FULLSCREEN = False#True
NOEXIT = False#True

FONTSIZE = 48
LINESIZE = 120
LEFTMAR = 30
TOPLOC = 90
