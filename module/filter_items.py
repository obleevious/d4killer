import numpy as nm
import time
import ctypes
import pyautogui

# importing OpenCV
import cv2
import easyocr

from PIL import ImageGrab
from module.item_evaluator import is_junk

reader = easyocr.Reader(["ch_sim"])

MOVE_DURATION = 0.5
ROW_NUM = 3
COL_NUM = 11
ORC_LANG = "chi_sim"
DEV_MODE = False
SE_FTR = (0.68, 0.72, 0.97, 0.86)
OFF_SET_X = (0, 74.3, 780, 850, 297, 371, 445, 519, 593, 668, 742)
OFF_SET_Y = (
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (-370, -265, -150),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0)
)
CLASS = "BARB"  # BARB, DURI, NECR, ROGU, SORC
SUB = ""  # TODO

def get_start_end_point():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    x, y = screensize
    return (x * SE_FTR[0], y * SE_FTR[1], x * SE_FTR[2], y * SE_FTR[3])

I, J, X, Y = get_start_end_point()

def get_current_position(a, b):
    if a % 2 == 0: b = 2 - b
    return I + ((X - I) / (COL_NUM - 1) * a), J + ((Y - J) / (ROW_NUM - 1) * b)

def get_item_details(a, b):
    cap = ImageGrab.grab(
        bbox=(
            1150 + OFF_SET_X[a],
            400 + OFF_SET_Y[a][b],
            1670 + OFF_SET_X[a],
            1065 + OFF_SET_Y[a][b],
        )
    )
    result = reader.readtext(cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY), detail=0)
    return result

def filter_current_item(a, b):
    x, y = get_current_position(a, b)
    print(x, y)
    pyautogui.moveTo(x, y, duration=MOVE_DURATION)
    time.sleep(MOVE_DURATION)
    item_details = get_item_details(a, b)
    if is_junk(item_details, CLASS, SUB):
        pyautogui.press("space")

def filter_items():
    pyautogui.moveTo(1600, 1036, duration=MOVE_DURATION)
    for a in range(COL_NUM):
        for b in range(ROW_NUM):
            filter_current_item(a, b)
            break
        break
