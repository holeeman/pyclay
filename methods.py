import cv2
import numpy as np
from PIL import Image
from PIL import ImageGrab
import pytesseract
import random

# global variables
base_directory = 'resource/'
window_x, window_y = (0, 0)
pre_width, pre_height = cv2.imread(base_directory + 'screen.png').shape[0:2][::-1]
new_width, new_height = cv2.imread(base_directory + 'new_screen.png').shape[0:2][::-1]
print new_width, new_height, pre_width, pre_height
ratio = new_width/float(pre_width), new_height/float(pre_height)


# this method returns randomly generated alphanumeric word
def random_name(max_length):
   length = random.randint(5, max_length)
   name = ""
   for x in range(length):
       r = random.randint(0, 59)
       if 0 <= r < 25:
           name += chr(65 + r % 25)
       elif 25 <= r < 50:
           name += chr(97 + (r - 25) % 25)
       elif r >= 50:
           name += str(r % 50)
   return name


# this method detects template from screen
def screen_detection(template, threshold=0.7, position=False):
    print pre_width, pre_height, new_width, new_height, ratio
    img = ImageGrab.grab([window_x, window_y, new_width, new_height])
    img = np.array(img, dtype=np.uint8)
    img = cv2.resize(img, (0, 0), fx=1 / ratio[0], fy=1 / ratio[1])
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #template = cv2.resize(template, (0,0), fx=ratio[0], fy=ratio[1])
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
    #cv2.imshow('Detected',img)
    #cv2.waitKey()
    if position:
        p = zip(*loc[::-1])[0]
        return (p[0] + w/2, p[1] + h/2)
    return len(zip(*loc[::-1])) > 0


# this method gets a captcha picture and returns OCRed word.
def anti_captcha(img):
    #cv2.imshow('', img)
    #cv2.waitKey()
    cropped_list = []

    kernel = np.ones((2, 2), np.uint8)
    img = cv2.medianBlur(img, 5)
    ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    img = 255 - img

    img = cv2.dilate(img, kernel, iterations=1)
    new_img = 255 - img

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3 , 3))
    dilated = cv2.dilate(img,kernel,iterations = 9)

    a, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

    for contour in contours:
        [x,y,w,h] = cv2.boundingRect(contour)

        if w < 35 and h<35:
            continue

        cropped_list.append([x, img[y:y + h, x: x + w]])
        cv2.rectangle(new_img,(x,y),(x+w,y+h),(0,0,0),2)

    cropped_list = sorted(cropped_list, key=lambda first: first[0])

    index = 0
    for im in cropped_list:
        cv2.imwrite('crop/' + str(index) + '.jpg', im[1])
        index += 1

    # write original image with added contours to disk
    #cv2.imshow('captcha_result' , new_img)
    #cv2.waitKey()

    string = ""
    for i in range(5):
        string += pytesseract.image_to_string(Image.open("crop/" + str(i) + ".jpg"), config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -psm 10')
    return string