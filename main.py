import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os, sys
import json
import time
import argparse

#################BOPO###################
bopos= {}
bopo_arr=['ㄓ','ㄕ','ㄖ','ㄗ','ㄙ','ㄚ','ㄛ','ㄜ','ㄞ','ㄟ','ㄠ','ㄡ','ㄢ','ㄣ','ㄤ','ㄥ','ㄦ','ㄧ',
'ㄧㄚ','ㄧㄝ','ㄧㄠ','ㄧㄡ','ㄧㄢ','ㄧㄣ','ㄧㄤ','ㄧㄥ','ㄨ','ㄨㄚ','ㄨㄛ','ㄨㄟ','ㄨㄢ','ㄨㄣ',
'ㄨㄤ','ㄨㄥ','ㄩ','ㄩㄝ','ㄩㄢ','ㄩㄣ']
bopo_size=36

with open('data.json') as f:
    mapping_list = json.load(f)

for i in range(38):
    # read template
    if (i==4): # skip
        continue
    img = cv.imread("bopomofo/%02d.jpg"%i)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    bopos[bopo_arr[i]] = img

def filterFcn(filterSymbol,sort=True):
    # Input: single character of bopomofo
    # Return List or None
    if filterSymbol in  ['ㄓ', 'ㄕ', 'ㄖ', 'ㄗ', 'ㄙ']:
         filterSymbol = ['ㄓ', 'ㄕ', 'ㄖ', 'ㄗ', 'ㄙ']
    else:
        filterSymbol = [filterSymbol]

    def fun(v): 
        if v["head"] in filterSymbol: 
            return True
        else: 
            return False
    result =  list(filter(fun, mapping_list))

    if sort is True:
        switcher={
            "normal": 0,
            "great": 1,
            "puricone": 2
        }
        result = sorted(result, key=lambda i: switcher[i["property"]], reverse=True)
    return result

def findBOPO(img):
    # Input image contain bopomofo character
    # Return single character of bopomofo
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    resized = cv.resize(img, (bopo_size,bopo_size), interpolation = cv.INTER_AREA)
    arr=[]
    for  bopo in bopos:
        res = cv.matchTemplate(resized,bopos[bopo],cv.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        arr.append((min_val, bopo))
    arr = sorted(arr, key= lambda x: x[0],reverse=True)
    return arr[0][1]

#################ICON###################
class Icon:
    id = None
    x = None
    y = None
    img = None

# Create icon mapping
# Usage: icons[ Icon ID ]
icons={}
icon_orig_size=78
icon_size=20
_ = cv.imread('icons.png')
with open("icons.csv","r") as f:
    for line in f.readlines():
        l = line.split(",")
        icon = Icon()
        icon.id=l[0]
        icon.x=abs(int(l[2]))
        icon.y=abs(int(l[1]))
        icon.img=_[icon.x:icon.x+icon_orig_size,icon.y:icon.y+icon_orig_size].copy()
        icon.img = cv.resize(icon.img, (icon_size,icon_size), interpolation = cv.INTER_AREA)
        icon.img= cv.cvtColor(icon.img, cv.COLOR_BGR2GRAY)
        icons[icon.id] = icon

def findIconId(img):
    # I suggest that it shouldn't convert whole image after read source image immediately, because it will take an extra time to process useless part.
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    resized = cv.resize(img, (icon_size,icon_size), interpolation = cv.INTER_AREA)
    arr=[]
    for icon in icons.values():
        # pattern matching
        # use 'min_val' or 'max_val as' smiliarity score
        res = cv.matchTemplate(resized,icon.img,cv.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        arr.append((min_val, icon.id))
    arr = sorted(arr, key= lambda x: x[0],reverse=True)
    # Maybe return false id cause I select a icon which has maximum 'min_val' among all icons
    return arr[0][1]

def test(img):
    # test if the image is a valid icon
    img=cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    ret, img=cv.threshold(img,200,255,cv.THRESH_BINARY)
    # step1: border exist
    left = img[5:6,5:-5]
    right = img[-5:-6,5:-5]
    top = img[5:-5,5:6]
    bottom = img[5:-5,-5:-6]
    count = cv.countNonZero(left) + cv.countNonZero(right) + cv.countNonZero(top) + cv.countNonZero(left) +cv.countNonZero(bottom)
    if count/4 < img.shape[0]*0.5:
        #print("Border doesn't exist")
        return False
    # setp2: white spot doesn't exist
    top_right = img[23:43,63:83]
    center = img[43:63,43:63]
    bottom_left = img[63:83,23:43]
    if cv.countNonZero(top_right)+cv.countNonZero(center)+cv.countNonZero(bottom_left)>= 3*400*0.95:
        #print("Broken image")
        return False
    return True

#################PARSER#################
def parse_args():

    # create parser
    parser = argparse.ArgumentParser(description='pcredive_game')
    
    # model parameters
    parser.add_argument('--input', help='The path of image')
    parser.add_argument('--output_x', help='x-coordinate', default=None)
    parser.add_argument('--output_y', help='y-coordinate', default=None)
    parser.add_argument('--debug', type=bool, help='The path of image',default=False)
    args = parser.parse_args()

    if args.input is None:
        print("insufficient arguments")
        sys.exit(-1)

    return args

#################MAIN###################

# Icon location
box_size=106
box_x = (249,368,486)
box_y = (119,236,354)

# Bopo location
bopo_x=328
bopo_y=897

# Start
args = parse_args()
img_path = args.input
output_x_path = args.output_x
output_y_path = args.output_y
debug_mode = args.debug
print("img path: %s\nx coord path:%s\ny coord path:%s\ndebug:%d"%(img_path,output_x_path,output_y_path,debug_mode))
input_img = cv.imread(img_path)

# Test if image is loaded completely
valid = True
for i in box_x:
    for j in box_y:
        icon_unknown = input_img[j:j+box_size,i:i+box_size]
        valid = valid&test(icon_unknown)
if valid is True:
    # mapping image to icon object
    icon_found = []
    for i in box_x:
        for j in box_y:
            icon_unknown = input_img[j:j+box_size,i:i+box_size]
            icon_found_id = findIconId(icon_unknown)
            icon_found.append((icon_found_id,i,j)) # (id, x, y)
    # identify bopomofo
    bopo_unknown = input_img[bopo_x:bopo_x+bopo_size,bopo_y:bopo_y+bopo_size]
    bopo_found = findBOPO(bopo_unknown)
    # select optimal solution
    answer_list = filterFcn(bopo_found)
    found_flag = False
    for ans in answer_list:
            if found_flag is True:
                break
            for icon in icon_found:
                if ans["icon_id"] == icon[0]:
                    found_flag = True
                    x = icon[1]
                    y = icon[2]
                    # output coordinates
                    if output_x_path is not None and output_x_path is not None:
                        with open(output_x_path,'w') as x_path, open(output_y_path, 'w') as y_path:
                            x_path.write("%d"%x)
                            y_path.write("%d"%y)
                    # debug
                    if debug_mode is True:
                        # For debugging
                        print("%s=> icon_id=%s, (%d,%d) %s: %s" %
                            (bopo_found,icon[0],x,y,ans["name"],ans["info"])
                        )
                        new_img = input_img.copy()
                        cv.rectangle(new_img,(x,y),(x+box_size,y+box_size), 255, 8)
                        cv.imshow("pic",new_img)
                        cv.waitKey()
                        sys.exit(0)
else:
    # output coordinates
    if output_x_path is not None and output_x_path is not None:
        with open(output_x_path,'w') as x_path, open(output_y_path, 'w') as y_path:
            x_path.write("%d"%-1)
            y_path.write("%d"%-1)
    if debug_mode is True:
        print("Invalid")
        sys.exit(-1)