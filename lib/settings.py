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
import save.saveStudent

USE = defaults.ONE_INCH
PHOTO = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../photo"
        )

PRINT_USE = defaults.THREE_R
PRINT = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../print"
        )

PRINTER = None

RAW = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../raw"
        )

ROT = False#True

SAVE = save.saveStudent.PhotoSave 
FILE = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../students.csv"
        )

FULLSCREEN = False#True
NOEXIT = False#True
