import numpy as nm
import time
import ctypes
import pyautogui

# importing OpenCV
import cv2
import easyocr
import random

from PIL import ImageGrab
from module.item_evaluator import is_junk

reader = easyocr.Reader(["ch_sim"])

# MOVE_DURATION = 0.5
MOVE_DURATION = 0
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
    (0, 0, 0),
)
CLASS = "BARB"  # BARB, DURI, NECR, ROGU, SORC
SUB = ""  # TODO
SAVE_IMG = False
READ_FROM_FILE = False


def get_start_end_point():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    x, y = screensize
    return (x * SE_FTR[0], y * SE_FTR[1], x * SE_FTR[2], y * SE_FTR[3])


I, J, X, Y = get_start_end_point()


def get_current_position(a, b):
    if a % 2 == 1:
        b = 2 - b
    return I + ((X - I) / (COL_NUM - 1) * a), J + ((Y - J) / (ROW_NUM - 1) * b)


def get_item_details(a, b):
    result = ""
    if not READ_FROM_FILE:
        cap = ImageGrab.grab(
            bbox=(
                1150 + OFF_SET_X[a],
                400 + OFF_SET_Y[a][b],
                1670 + OFF_SET_X[a],
                1065 + OFF_SET_Y[a][b],
            )
        )
        if SAVE_IMG:
            cap.save("./temp/" + str(a) + "_" + str(b) + ".png")
        result = reader.readtext(nm.array(cap), detail=0)
    else:
        result = reader.readtext(
            "./temp_back/" + str(a) + "_" + str(b) + ".png", detail=0, paragraph=1
        )
    return result


def move_mouse_plus(x, y):
    pyautogui.moveTo(x, y, duration=MOVE_DURATION)
    for i in range(5):
        r = random.randint(-3, 3)
        q = random.randint(-3, 3)
        pyautogui.moveTo(x + r, y + q)
    pyautogui.moveTo(x, y, duration=0.1)


def filter_current_item(a, b):
    x, y = get_current_position(a, b)
    move_mouse_plus(x, y)

    time.sleep(MOVE_DURATION)
    item_details = get_item_details(a, b)
    if is_junk(item_details, CLASS, SUB):
        print("Junk!")
        pyautogui.press("space")


def filter_items():
    pyautogui.moveTo(1600, 1036, duration=MOVE_DURATION)
    for a in range(COL_NUM):
        for b in range(ROW_NUM):
            filter_current_item(a, b)
        #     break
        # break
