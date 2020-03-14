import cv2 as cv
import numpy as np
healthbar_full = cv.imread("./template/healthbar_full.jpg")

def full(img):
    crop = img[
        30:30+10,
        928:928+200,
    ].copy()
    imgray = cv.cvtColor(crop,cv.COLOR_RGB2GRAY)
    _ , thresh = cv.threshold(imgray,174, 255, 0)
    kernel = np.ones((3, 3), np.uint8) 
    thresh = cv.erode(thresh, kernel)    
    pixel_nzero = cv.countNonZero(thresh)

    if pixel_nzero > 1950:
        return True
    return False