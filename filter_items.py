# cv2.cvtColor takes a numpy ndarray as an argument
import sys
import numpy as nm
import time
import ctypes
import pyautogui
# importing OpenCV
import cv2
import easyocr

from PIL import ImageGrab
from pynput import keyboard

reader = easyocr.Reader(['ch_sim'])

MOVE_DURATION = 0.5
ROW_NUM = 3
COL_NUM = 11
ORC_LANG = 'chi_sim'
DEV_MODE = False
SE_FTR = (0.68, 0.72, 0.97, 0.86)
OFF_SET = (0, 74.3, 780)

def get_current_position(a, b):
    i, j, x, y = get_start_end_point()
    print(i,j,x,y)
    return i + ((x-i)/(COL_NUM-1) * a), j + ((y-j)/(ROW_NUM-1) * b)

def is_junk(item_details):
    print(item_details)
    return True

def get_item_details(a, b):
    cap = ImageGrab.grab(bbox =(1150 + OFF_SET[a], 400, 1670 + OFF_SET[a], 1065))
    # cap = ImageGrab.grab(bbox =(605, 265, 855, 295))
    cap.show()
    result = reader.readtext(cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY), detail = 0)
    return result
    # return ""

def filter_current_item(a, b):
    x, y = get_current_position(a, b)
    print(x, y)
    pyautogui.moveTo(x, y, duration = MOVE_DURATION)
    time.sleep(MOVE_DURATION)
    item_details = get_item_details(a, b)
    if is_junk(item_details):
        pyautogui.press("space")

def filter_items():
    pyautogui.moveTo(1600, 1036, duration = MOVE_DURATION)
    # for a in range(COL_NUM):
    for a in range(2, COL_NUM):
        for b in range(ROW_NUM):
            filter_current_item(a, b)
            break
        break

def get_start_end_point():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    x, y = screensize
    return (x * SE_FTR[0], y * SE_FTR[1], x * SE_FTR[2], y * SE_FTR[3])

def on_press(key):
    if key == keyboard.Key.esc:
        sys.exit()
    if key == keyboard.Key.backspace:
        filter_items()

def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys

def main():
    start_listener()
    # filter_items()

if __name__ == "__main__":
    main()
