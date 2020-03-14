import cv2 as cv
import json
import icon

bopos= {}
bopo_arr=['ㄓ','ㄕ','ㄖ','ㄗ','ㄙ','ㄚ','ㄛ','ㄜ','ㄞ','ㄟ','ㄠ','ㄡ','ㄢ','ㄣ','ㄤ','ㄥ','ㄦ','ㄧ',
'ㄧㄚ','ㄧㄝ','ㄧㄠ','ㄧㄡ','ㄧㄢ','ㄧㄣ','ㄧㄤ','ㄧㄥ','ㄨ','ㄨㄚ','ㄨㄛ','ㄨㄟ','ㄨㄢ','ㄨㄣ',
'ㄨㄤ','ㄨㄥ','ㄩ','ㄩㄝ','ㄩㄢ','ㄩㄣ']

identified_char = None
large_icon_id = None

large_icon_mask = cv.imread('template/large_icon_mask.jpg',cv.IMREAD_GRAYSCALE)

with open('data.json') as f:
    mapping_list = json.load(f)

for i in range(len(bopo_arr)):
    # read template
    if (i==4): # skip 'ㄙ', because we don't have this picture
        continue
    img = cv.imread("bopomofo/%02d.jpg"%i)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    bopos[bopo_arr[i]] = img

def test_right(img):
    crop = img[
        196:196+187,
        765:765+187,
    ].copy()
    imgray = cv.cvtColor(crop,cv.COLOR_RGB2GRAY)
    res = cv.bitwise_and(imgray,large_icon_mask)
    _ , thresh = cv.threshold(res, 240, 255, 0)
    pixel_nzero = cv.countNonZero(thresh)
    if pixel_nzero >3000:
        return crop.copy()
    return False

def test_left(img):
    crop = img[
        196:196+187,
        328:328+187,
    ].copy()
    imgray = cv.cvtColor(crop,cv.COLOR_RGB2GRAY)
    res = cv.bitwise_and(imgray,large_icon_mask)
    _ , thresh = cv.threshold(res, 240, 255, 0)
    pixel_nzero = cv.countNonZero(thresh)
    if pixel_nzero >3000:
        return crop.copy()
    return False

def test(img):
    # test if the image has a valid large icon
    result = test_left(img)
    if result is False:
        result = test_right(img)
    if result is False:
        return False
    
    # Input image contain large icon
    # Save it
    crop=result[10:10+168,10:10+84]
    crop = cv.cvtColor(crop, cv.COLOR_BGR2GRAY) 
    resized = cv.resize(crop, 
        (
            int(icon.icon_new_size/2),
            icon.icon_new_size
        ),   
        interpolation = cv.INTER_AREA)
    arr=[]
    for icon_ in icon.icons.values():
        new_icon_img = icon_.img[
            0:icon.icon_new_size,
            0:int(icon.icon_new_size/2)
        ].copy()
        res = cv.matchTemplate(resized,new_icon_img,cv.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        arr.append((min_val, icon_.id, new_icon_img))
    arr = sorted(arr, key= lambda x: x[0],reverse=True)
    global large_icon_id
    large_icon_id = arr[0][1]

    # Input image contain bopomofo character
    # Save single character of bopomofo
    bopo_x=133
    bopo_y=131
    bopo_size=36
    crop = result[bopo_x:bopo_x+bopo_size,bopo_y:bopo_y+bopo_size]
    crop = cv.cvtColor(crop, cv.COLOR_BGR2GRAY) 
    arr=[]
    for  bopo in bopos:
        res = cv.matchTemplate(crop,bopos[bopo],cv.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        arr.append((min_val, bopo))
    arr = sorted(arr, key= lambda x: x[0],reverse=True)
    global identified_char
    identified_char = arr[0][1]

    return True

def getCandidate(filterSymbol=identified_char,sort=True):
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

