import cv
import sys

def get_image():
    cam = cv.CaptureFromCAM(0)
    cv_im = cv.QueryFrame(cam)
    del cam
    return cv_im

