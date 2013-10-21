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

import sys, os, wx
import cv2.cv as cv
import lib.settings as settings
import lib.process as process
import lib.util as util

def choosePrinter():
    print '是否导出打印文件？(y/N): ',
    get = raw_input()
    if get and (get[0] == 'Y' or get[0] == 'y'):
        return settings.PRINTER
    else:
        return None

def chooseUse():
    for i in xrange(len(settings.USES)):
        print '*', i, ':', settings.USES[i]["name"]
    print '输入数字选择导出照片格式 (空白为 0): ',
    try: get = raw_input(); get=0 if not get else int(get)
    except Exception: get = -1
    while get >= len(settings.USES) or get < 0:
        print '重新输入数字选择导出照片格式: ',
        try: get = raw_input(); get=0 if not get else int(get)
        except Exception: get = -1
    return settings.USES[get]

def choosePrintMedia():
    for i in xrange(len(settings.PRINT_USES)):
        print '*', i, ':', settings.PRINT_USES[i]["name"]
    print '输入数字选择打印照片介质 (空白为 0): ',
    try: get = raw_input(); get=0 if not get else int(get)
    except Exception: get = -1
    while get >= len(settings.USES) or get < 0:
        print '重新输入数字选择打印照片介质: ',
        try: get = raw_input(); get=0 if not get else int(get)
        except Exception: get = -1
    return settings.PRINT_USES[get]

def chooseEffect():
    print '*', 0, ':', '普通' 
    print '*', 1, ':', '黑白'
    print '输入数字选择导出照片效果 (空白为 0): ',
    try: get = raw_input(); get=0 if not get else int(get)
    except Exception: get = -1
    while get >= 2 or get < 0:
        print '重新输入数字选择导出照片效果: ',
        try: get = raw_input(); get=0 if not get else int(get)
        except Exception: get = -1
    return get == 1

try:
    if __name__ == '__main__': 
        print "人像采集系统[后台管理]"
        if len(sys.argv) > 1:
            settings.FILE = sys.argv[1]
            once = False
        else:
            once = True
        fmt = settings.FMT
        rawd = settings.RAW
        use = chooseUse()
        effect = chooseEffect()
        printer = choosePrinter()
        if printer: prMedia = choosePrintMedia()
        else: prMedia = None
        saver = settings.SAVE(
                settings.FILE, settings.PHOTO,
                settings.FMT, settings.RAW,
                settings.PRINT, printer, True)
        if once:
            print "输入需处理照片的编号: ", 
            getid = raw_input().strip()
            saver.current = (getid, getid)
        current = 0
        tot = saver.remain
        while saver.filename():
            current += 1
            print "正在导出: [%d/%d] %s: %s" % (
                    current, tot,
                    saver.name(), saver.filename() )
            try:
                raw = cv.LoadImage(os.path.join(rawd,
                    saver.filename() + fmt))
            except:
                print "出现错误，文件不存在"
                saver.nextStudent()
                continue
            photo = process.getPhoto(raw, use)
            if effect:
                newphoto = cv.CreateImage((photo.width, photo.height), 8, 1)
                cv.CvtColor(photo, newphoto, cv.CV_BGR2GRAY)
                cv.CvtColor(newphoto, photo, cv.CV_GRAY2BGR)
            if prMedia and printer:
                printable = process.getPrint(photo, prMedia, saver.filename())
                saver.save(None, None, printable)
            else:
                saver.save(photo, None, None)
except KeyboardInterrupt:
    print "任务已取消"
