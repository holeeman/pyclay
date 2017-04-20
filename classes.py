import pyautogui
import time
import cv2
import threading
from methods import *
state = None
mouse_pos = pyautogui.position()
lock = threading.Lock()


class State:
    def __init__(self, macros=list()):
        self.macro_list = macros
        self.loop_break = False
        self.on_break = None

    def set(self, macros):
        self.macro_list = macros

    def add(self, macro):
        self.macro_list.append(macro)

    def execute(self):
        for m in self.macro_list:
            print str(m.__class__).replace("classes.", "")
            if self.loop_break:
                print "break"
                if self.on_break:
                    self.on_break.run()
                break
            m.run()
            if m.__class__ == Goto:
                print "end"
                break


class Click:
    def __init__(self, x, y, r=True):
        if r:
            self.x, self.y = [x * ratio[0], y * ratio[1]]
        else:
            self.x, self.y = [x, y]
    def run(self):
        pyautogui.click(self.x, self.y)


class ClickPic:
    def __init__(self, image, pos=(0, 0), r=True):
        if r:
            self.image, self.pos = [cv2.imread(base_directory + image, 0), (pos[0] * ratio[0], pos[1] * ratio[1])]
        else:
            self.image, self.pos = [cv2.imread(base_directory + image, 0), (pos[0], pos[1])]

    def run(self):
        p =  screen_detection(self.image, position=True)
        pyautogui.click(p[0] + self.pos[0], p[1] + self.pos[1])


class Drag:
    def __init__(self, x1, y1, x2, y2, r=True, d=0):
        if r:
            self.x1, self.y1, self.x2, self.y2 = [x1 * ratio[0], y1 * ratio[1], x2 * ratio[0], y2 * ratio[1]]
        else:
            self.x1, self.y1, self.x2, self.y2 = [x1, y1, x2, y2]
        self.d = d

    def run(self):
        pyautogui.moveTo(self.x1, self.y1)
        pyautogui.dragTo(self.x2, self.y2, self.d)


class Type:
    def __init__(self, string):
        self.string = string

    def run(self):
        pyautogui.typewrite(self.string)


class KeyDown:
    def __init__(self, key):
        self.key = key

    def run(self):
        pyautogui.keyDown(self.key)


class KeyUp:
    def __init__(self, key):
        self.key = key

    def run(self):
        pyautogui.keyUp(self.key)


class Wait:
    def __init__(self, time):
        self.time = time

    def run(self):
        time.sleep(self.time)


class Match:
    def __init__(self, template, success, fail, threshold=0.75):
        self.name = template
        self.template, self.success, self.fail, self.threshold = [template, success, fail, threshold]
        self.template = cv2.imread(base_directory + self.template, 0)

    def run(self):
        print "detecting", self.name,"..."
        if screen_detection(self.template, self.threshold):
            print "Match Success"
            self.success.run()
        else:
            print "Match Fail"
            self.fail.run()


class Captcha:
    def __init__(self):
        #self.success, self.fail = [success, fail]
        pass

    def run(self):
        img = ImageGrab.grab([window_x + 98 * ratio[0], window_y + 835 * ratio[1], window_x + 536 * ratio[0], window_y + 947 * ratio[1]])
        img = np.array(img, dtype=np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        capt_word = anti_captcha(img)
        pyautogui.click(214 * ratio[0], 1003 * ratio[1])
        pyautogui.typewrite(capt_word)


class Goto:
    def __init__(self, state):
        self.state = state

    def run(self):
        global state
        state = self.state
        state.execute()


class Log:
    def __init__(self, string):
        self.string = string

    def run(self):
        print self.string


class Timer:
    def __init__(self, time, macro):
        self.time, self.macro = [time, macro]
        self.current_state = state
        self.t = threading.Thread(target=self.timer)
        self.t.daemon = True

    def timer(self):
        time.sleep(self.time)
        lock.acquire()
        state.on_break = self.macro
        state.loop_break = True
        lock.release()
        # self.macro.run()

    def run(self):
        self.t.start()
