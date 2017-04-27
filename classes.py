import pyautogui
import time as pytimer
import cv2
import threading
import Queue
from methods import *
state = None
state_queue = Queue.Queue()
lock = threading.Lock()
timers = []
default = None
on_start = None
ratio = [1, 1]


def execute(state_to_execute, state_on_execute=None):
    if state_on_execute and not state_to_execute.ignore:
        State.on_execute= state_on_execute.macro_list
    for m in State.on_execute:
        state_queue.put(m)
    for m in state_to_execute.macro_list:
        state_queue.put(m)
    while not state_queue.empty():
        m = state_queue.get()
        print m.__class__
        m.run()


class State:
    on_execute = []

    def __init__(self, macros=list(), ignore=False):
        self.macro_list = macros
        self.ignore = ignore

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
    def __init__(self, image, pos=(0, 0), r=True, threshold=0.7):
        if r:
            self.image, self.pos = [cv2.imread(base_directory + image, 0), (pos[0] * ratio[0], pos[1] * ratio[1])]
        else:
            self.image, self.pos = [cv2.imread(base_directory + image, 0), (pos[0], pos[1])]
        self.thres = threshold

    def run(self):
        p = screen_detection(self.image, threshold=self.thres, position=True)
        print p
        if p[0] < 0:
            print "picture not detected"
            return
        pyautogui.click(window_x + p[0] * ratio[0] + self.pos[0], window_y + p[1] * ratio[1] + self.pos[1])


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
        pytimer.sleep(self.time)


class Match:
    def __init__(self, template, success, fail, threshold=0.75, t=0):
        self.name, self.t = [template, t]
        self.template, self.success, self.fail, self.threshold = [template, success, fail, threshold]
        self.template = cv2.imread(base_directory + self.template, 0)

    def run(self):
        print "detecting", self.name, "..."
        current_time = pytimer.time()
        res = False

        if self.t == 0:
            if screen_detection(self.template, self.threshold):
                res = True
        while self.t > 0 and pytimer.time() - current_time < self.t:
            if screen_detection(self.template, self.threshold):
                res = True
                break
            pytimer.sleep(0.1)

        if res:
            print "Match Success"
            self.success.run()
        else:
            print "Match Fail"
            self.fail.run()


class Goto:
    def __init__(self, state_to_execute):
        self.state = state_to_execute

    def run(self):
        with state_queue.mutex:
            state_queue.queue.clear()

        with lock:
            if not self.state.ignore:
                for m in State.on_execute:
                    state_queue.put(m)
            for m in self.state.macro_list:
                state_queue.put(m)


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
        pytimer.sleep(self.time)
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

    def run(self):
        pass


class Execute:
    def __init__(self, function):
        self.function = function

    def run(self):
        self.function()
