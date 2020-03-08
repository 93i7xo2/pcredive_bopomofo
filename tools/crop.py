import cv2 as cv

#location = [897, 329] # right
location = [459, 329] # left

size=[36,36]
x1=location[0]
x2=x1+size[0]
y1=location[1]
y2=y1+size[1]

import os

count = 0
for r, d, f in os.walk('.'):
    for file in f:
        if '.jpg' in file:
            path = os.path.join(r, file)
            im = cv.imread(path)
            corp = im[y1:y2,x1:x2]
            cv.imwrite("%02d.jpg"%count,corp)
            count  = count +1
