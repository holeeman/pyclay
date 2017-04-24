import pyautogui
import time
import cv2
import threading
import Queue
from methods import *
state = None
state_queue = Queue.Queue()
lock = threading.Lock()
timers = []
default = None


def execute(state_to_execute):
    for m in state_to_execute.macro_list:
        state_queue.put(m)
    while not state_queue.empty():
        m = state_queue.get()
        print m.__class__
        m.run()


class State:
    def __init__(self, macros=list()):
        self.macro_list = macros
        self.loop_break = False
        self.on_break = None

    def set(self, macros):
        self.macro_list = macros

    def add(self, macro):
        self.macro_list.append(macro)


class Click:
    def __init__(self, x, y, r=True, d=False):
        if r:
            self.x, self.y = [x * ratio[0], y * ratio[1]]
        else:
            self.x, self.y = [x, y]
        self.d = d

    def run(self):
        if self.d:
            pyautogui.doubleClick(self.x, self.y)
        else:
            pyautogui.click(self.x, self.y)



class ClickPic:
    def __init__(self, image, pos=(0, 0), r=True):
        if r:
            self.image, self.pos = [cv2.imread(base_directory + image, 0), (pos[0] * ratio[0], pos[1] * ratio[1])]
        else:
            self.image, self.pos = [cv2.imread(base_directory + image, 0), (pos[0], pos[1])]

    def run(self):
        p = screen_detection(self.image, position=True)
        if p[0] < 0:
            print "picture not detected"
            return
        pyautogui.click(p[0] * ratio[0] + self.pos[0], p[1] * ratio[1] + self.pos[1])


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
    def __init__(self, template, success, fail, threshold=0.75, t=0):
        self.name, self.t = [template, t]
        self.template, self.success, self.fail, self.threshold = [template, success, fail, threshold]
        self.template = cv2.imread(base_directory + self.template, 0)

    def run(self):
        print "detecting", self.name, "..."
        current_time = time.time()
        res = False

        if self.t == 0:
            if screen_detection(self.template, self.threshold):
                res = True
        while self.t > 0 and time.time() - current_time < self.t:
            if screen_detection(self.template, self.threshold):
                res = True
                break
            time.sleep(0.1)

        if res:
            print "Match Success"
            self.success.run()
        else:
            print "Match Fail"
            self.fail.run()


class Captcha:
    def __init__(self):
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
        with state_queue.mutex:
            state_queue.queue.clear()
        for m in self.state.macro_list:
            lock.acquire()
            state_queue.put(m)
            lock.release()


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
        self.running = False
        self.off = False

    def timer(self):
        time.sleep(self.time)
        timers.remove(self)
        if self.off:
            return
        with state_queue.mutex:
            state_queue.queue.clear()
        lock.acquire()
        state_queue.put(self.macro)
        lock.release()
        # self.macro.run()

    def run(self):
        timers.append(self)
        if not self.running:
            self.running = True
            self.t.start()


class TimerOff:
    def __init__(self):
        pass

    def run(self):
        for t in timers:
            t.off = True


class Comment:
    def __init__(self, comment):
        pass
