import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import sys
import json
import time
import argparse
import icon
import bopo
import tools
import healthbar

# Load table
with open("findPairInRoundTable.json") as f:
    tools.findPairInRoundTable = json.load(f)

# Load database
with open("DB.json", encoding='utf8') as f:
    db = json.load(f)


def parse_args():

    # create parser
    parser = argparse.ArgumentParser(description='pcredive_game')

    # model parameters
    parser.add_argument('--input', help='The path of image')
    parser.add_argument('--debug', type=bool,
                        help='The path of image', default=False)
    args = parser.parse_args()

    if args.input is None:
        print("insufficient arguments")
        sys.exit(-1)
    return args


args = parse_args()
img_path = args.input
debug_mode = args.debug
input_img = cv.imread(img_path)


def getAvailableInfo():
    return list(filter(lambda info: db[info] == False, db))


# Test if image is loaded completely
t = time.time()
Round = 0
pre_identified_char = None
if bopo.test(input_img) is True and icon.test(input_img) is True:
    # Identify bopomofo and 9 icons
    # A identified character will be saved in 'bopo.identified_char'
    # A identified large IconID will be saved in 'bopo.large_icon_id'
    # Icon objects will be saved in 'icon.icon_found'

    if healthbar.full(input_img) is True:
        # Round 1, gp=100%
        print("HP 100%")
        Round = 1
        pre_identified_char = bopo.identified_char
    elif pre_identified_char != bopo.identified_char:
        # Not Round 1, increase it.
        pre_identified_char = bopo.identified_char
        Round = Round + 1

    # Find a icon whose icon-id is in the list
    answers = bopo.getCandidate(bopo.identified_char)
    for i in icon.icon_found:
        # whether this icon can be chosen
        m = list(filter(lambda ans: ans["icon_id"] == i.id, answers))
        if len(m) == 0:
            i.qualified = False
            continue
        i.qualified = True

        head = m[0]["head"]
        tail = m[0]["tail"]
        info = m[0]["info"]

        if db[info] is False:
            # I never meet this info before and can choose it.
            i.p_list = (info, (1, tail))  # info, (possibility, tail)
            continue

        # Caculate the possibility.
        tmp_list = []
        for a_info in getAvailableInfo():
            tmp_list.append(
                (
                    # info, (possibility, tail)
                    a_info,
                    tools.findPairInRound(
                        tail,
                        a_info,
                        Round+1
                    )
                )
            )
        # sort
        tmp_list = sorted(tmp_list, key=lambda x: x[1], reverse=True)
        if len(tmp_list) > 0:
            # still havs an info that has never been selected
            i.p_list = tmp_list[0][:]  # copy this

    # Show image
    img = input_img.copy()
    for i in icon.icon_found:
        if i.qualified is not True:
            continue
        info = i.p_list[0]
        probability = float(i.p_list[1][0])*100 # 0~100%
        tail = i.p_list[1][1]

        print(i.p_list)

        Color = [
            # B,G,R
            (0, 0, 255),  # Red, 100%
            (0, 165, 255),  # Orange, 0~100%
            (128, 128, 128)  # Gray, 0%
        ]
        font = cv.FONT_HERSHEY_SIMPLEX
        fontScale = 0.8
        thickness = 2

        base_x = icon.icon_box_location[0]
        base_y = icon.icon_box_location[1]

        img_text = "%.1f%%" % probability
        if probability == 100:
            color = Color[0]
        elif probability > 0:
            color = Color[1]
        else:
            color = Color[2]

        cv.putText(
            img,
            img_text,
            (base_y+i.y, base_x+i.x+50),
            font,
            fontScale,
            color,
            thickness)
        cv.rectangle(
            img,
            (i.y+base_y,i.x+base_x), 
            (i.y+icon.icon_size+base_y, i.x+icon.icon_size+base_x),
            color,
            4)
    cv.imshow("Result", img)
    cv.waitKey()
    # Draw
    #         # For debugging
    #         new_img = input_img.copy()
    #
    #         cv.imshow("pic",new_img)
    #         cv.waitKey()
    #         sys.exit(0)
else:
    print("Invalid")
    sys.exit(-1)
print(time.time()-t)
