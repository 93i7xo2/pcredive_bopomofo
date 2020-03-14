import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os, sys
import json
import time
import argparse
import icon
import bopo

def parse_args():

    # create parser
    parser = argparse.ArgumentParser(description='pcredive_game')
    
    # model parameters
    parser.add_argument('--input', help='The path of image')
    parser.add_argument('--debug', type=bool, help='The path of image',default=False)
    args = parser.parse_args()

    if args.input is None:
        print("insufficient arguments")
        sys.exit(-1)

    return args

args = parse_args()
img_path = args.input
debug_mode = args.debug
input_img = cv.imread(img_path)

# Test if image is loaded completely
# If it pass the test, icon objects will be saved in 'icon_found'
valid = icon.test(input_img)
if valid is True:
    # Identify bopomofo
    # A identified character will be saved in 'identified_char'
    bopo.test(input_img)

    # select optimal solution
    answer_list = filterFcn(bopo.identified_char)

    found_flag = False
    for ans in answer_list:
            # if found_flag is True:
            #     break
            # for icon in icon_found:
            #     if ans["icon_id"] == icon[0]:
            #         found_flag = True
            #         x = icon[1]
            #         y = icon[2]
            #         print("%s=> icon_id=%s, (%d,%d) %s: %s" %
            #         (bopo_found,icon[0],x,y,ans["name"],ans["info"])
            #         )

            #         # For debugging
            #         new_img = input_img.copy()
            #         cv.rectangle(new_img,(x,y),(x+box_size,y+box_size), 255, 8)
            #         cv.imshow("pic",new_img)
            #         cv.waitKey()
            #         sys.exit(0)
else:
    print("Invalid")
    sys.exit(-1)