import cv2 as cv
import json

bopos= {}
bopo_arr=['ㄓ','ㄕ','ㄖ','ㄗ','ㄙ','ㄚ','ㄛ','ㄜ','ㄞ','ㄟ','ㄠ','ㄡ','ㄢ','ㄣ','ㄤ','ㄥ','ㄦ','ㄧ',
'ㄧㄚ','ㄧㄝ','ㄧㄠ','ㄧㄡ','ㄧㄢ','ㄧㄣ','ㄧㄤ','ㄧㄥ','ㄨ','ㄨㄚ','ㄨㄛ','ㄨㄟ','ㄨㄢ','ㄨㄣ',
'ㄨㄤ','ㄨㄥ','ㄩ','ㄩㄝ','ㄩㄢ','ㄩㄣ']

identified_char = None

with open('data.json') as f:
    mapping_list = json.load(f)

for i in range(len(bopo_arr)):
    # read template
    if (i==4): # skip 'ㄙ', because we don't have this picture
        continue
    img = cv.imread("bopomofo/%02d.jpg"%i)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    bopos[bopo_arr[i]] = img

def test(img):
    bopo_x=328
    bopo_y=897
    bopo_size=36
    crop = img[bopo_x:bopo_x+bopo_size,bopo_y:bopo_y+bopo_size]

    # Input image contain bopomofo character
    # Save single character of bopomofo
    crop = cv.cvtColor(crop, cv.COLOR_BGR2GRAY) 
    arr=[]
    for  bopo in bopos:
        res = cv.matchTemplate(img,bopos[bopo],cv.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        arr.append((min_val, bopo))
    arr = sorted(arr, key= lambda x: x[0],reverse=True)
    global identified_char
    identified_char = [0][1]


def getCandidate(filterSymbol,sort=True):
    # Input: single character of bopomofo
    # Return candidate List or None
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

