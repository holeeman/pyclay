import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import time as asdf
#import pyscreenshot as ImageGrab

# global variables
base_directory = './resource/'
window_x = 596
window_y = 347
# debug = False

# this method detects template from screen
def screen_detection(template, threshold=0.7, position=False, debug=False):
    # print pre_width, pre_height, new_width, new_height, ratio
    try:
        img = pyautogui.screenshot(region=[596, 347, 1114, 1312])
    except IOError:
        if position:
            print "IO ERROR: position"
            return [-1, -1]
        else:
            print "IO ERROR: BOOL"
            return False

    img = np.array(img, dtype=np.uint8)
    #img = cv2.resize(img, (0, 0), fx=1 / ratio[0], fy=1 / ratio[1])
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # template = cv2.resize(template, (0,0), fx=ratio[0], fy=ratio[1])
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
    if debug:
        cv2.imshow('Detected',img)
        cv2.waitKey()

    if position:
        p = zip(*loc[::-1])
        if len(p) == 0:
            return [-1, -1]
        return (p[0][0] + w/2, p[0][1] + h/2)
    return len(zip(*loc[::-1])) > 0