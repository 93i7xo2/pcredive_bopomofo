import cv2 as cv

class Icon:
    id = None
    x = None
    y = None
    img = None

class Icon2:
    id = None
    x = None
    y = None
    qualified = None
    p_list = None
    def __init__(self,icon_id,x=-1,y=-1):
        self.id = icon_id
        self.x = x
        self.y = y 

icon_box_location = [None, None] # Defined in function test()
icon_box_size = 354
icon_size = 96
icon_location = [
    [10, 12],
    [10, 130],
    [10, 248],
    [129, 12],
    [129, 130],
    [129, 248],
    [247, 12],
    [247, 130],
    [247, 248],
]

icon_found = None

icon_box_mask = cv.imread("./template/icon_box_mask.jpg",cv.IMREAD_GRAYSCALE)

# Create icon mapping
# Usage: icons[ Icon ID ]
icons={}
icon_orig_size=78
icon_new_size=52
_ = cv.imread('icons.png')
with open("icons.csv","r") as f:
    for line in f.readlines():
        l = line.split(",")
        icon = Icon()
        icon.id=l[0]
        icon.x=abs(int(l[2]))
        icon.y=abs(int(l[1]))
        icon.img=_[icon.x+4:icon.x+icon_orig_size-4,icon.y+4:icon.y+icon_orig_size-4].copy()
        # copy icon and eliminate white broder
        icon.img = cv.resize(icon.img, (icon_new_size,icon_new_size), interpolation = cv.INTER_AREA)
        icon.img= cv.cvtColor(icon.img, cv.COLOR_BGR2GRAY)
        icons[icon.id] = icon

def findIconId(img):
    # I suggest that it shouldn't convert whole image after read source image immediately, because it will take an extra time to process useless part.
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
    resized = cv.resize(img, (icon_new_size,icon_new_size), interpolation = cv.INTER_AREA)
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

def mappingImage2Icon(img):
    global icon_found
    icon_found = []
    for (x,y) in icon_location:
            icon_unknown = img[x:x+icon_size,y:y+icon_size]
            icon_found_id = findIconId(icon_unknown)
            icon_found.append(Icon2(icon_found_id,x,y))

def test(img):
    # test if the image is a valid icon
    global icon_box_location

    # Left
    icon_box_location = [113,243]
    crop = img[
        icon_box_location[0]:icon_box_location[0]+icon_box_size,
        icon_box_location[1]:icon_box_location[1]+icon_box_size,
    ]
    imgray = cv.cvtColor(crop,cv.COLOR_RGB2GRAY)
    res = cv.bitwise_and(imgray,icon_box_mask)
    _ , thresh = cv.threshold(res, 127, 255, 0)
    pixel_nzero = cv.countNonZero(thresh)
    if pixel_nzero < 300: # 20->300 
        mappingImage2Icon(crop)
        return True

    # Right
    icon_box_location = [113,681]
    crop = img[
        icon_box_location[0]:icon_box_location[0]+icon_box_size,
        icon_box_location[1]:icon_box_location[1]+icon_box_size,
    ]
    imgray = cv.cvtColor(crop,cv.COLOR_RGB2GRAY)
    res = cv.bitwise_and(imgray,icon_box_mask)
    _ , thresh = cv.threshold(res, 127, 255, 0)
    pixel_nzero = cv.countNonZero(thresh)
    if pixel_nzero < 300:
        mappingImage2Icon(crop)
        return True
    
    return False
