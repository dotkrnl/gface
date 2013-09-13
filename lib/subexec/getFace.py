#!/usr/bin/env python2.7
import cv2.cv as cv
import sys
import os

cas = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "face_cascade.xml"
)

def detectFace(image):
    grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

    cascade = cv.Load(cas)
    rect = cv.HaarDetectObjects(grayscale, cascade,
            cv.CreateMemStorage(), 1.1, 2,
            cv.CV_HAAR_DO_CANNY_PRUNING, (20,20))
    
    result = (0, 0, 0, 0)
    for r in rect:
        if result[2] * result[3] < r[0][2] * r[0][3]:
            result = r[0]
    if result[0]: return result
    else: return None

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Usage: %s [file]." % sys.argv[0]
        sys.exit(1)
    filename = sys.argv[1]
    image = cv.LoadImage(filename)
    face = detectFace(image)
    if face:
        print face[0], face[1]
        print face[2], face[3]
    else:
        sys.exit(1)
