# cv2.cvtColor takes a numpy ndarray as an argument
import sys
import numpy as nm
import time
import pytesseract
import ctypes
import pyautogui
# importing OpenCV
import cv2

from PIL import ImageGrab
from pynput import keyboard

TESSEARACT_ROOT = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
MOVE_DURATION = 0.2
ROW_NUM = 3
COL_NUM = 11
ORC_LANG = 'chi_sim'

# Path of tesseract executable
pytesseract.pytesseract.tesseract_cmd = TESSEARACT_ROOT

def get_current_position(a, b):
    i, j, x, y = get_start_end_point()
    return i + ((x-i)/(COL_NUM-1) * a), j + ((y-j)/(ROW_NUM-1) * b)

def isGoodItem():
    return False

def get_item_details(a, b):
    cap = ImageGrab.grab(bbox =(605, 215, 855, 675)) 
    # cap = ImageGrab.grab(bbox =(605, 265, 855, 295))

    # print(nm.array(cap))
    
    # cv2.imshow("window_name", cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY))

    # imToString(cap)

    tesstr = pytesseract.image_to_string(
        cap, 
        lang = ORC_LANG)
    
    print(tesstr)
    cap.show()

def filter_current_item(a, b):
    x, y = get_current_position(a, b)
    print(x, y)
    pyautogui.moveTo(x, y, duration = MOVE_DURATION)
    time.sleep(MOVE_DURATION)
    item_details = get_item_details(a, b)
    if not isGoodItem():
        pyautogui.keyDown("space")

def filter_items():
    for a in range(COL_NUM):
        for b in range(ROW_NUM):
            filter_current_item(a, b)
            break
        break

def get_start_end_point():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    x, y = screensize
    print(x, y)
    return (x * 0.34375, y * 0.36111, x * 0.4854, y * 0.4305)

def imToString(cap):
    print(pytesseract.get_languages())
    tesstr = pytesseract.image_to_string(
            cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY), 
            lang = ORC_LANG)
    print(tesstr)
  
def on_press(key):
    if key == keyboard.Key.esc:
        sys.exit()
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'backspace':
        filter_items()
        # return False  

def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys

def main():
    start_listener()
    # filter_items()

    # pyautogui.moveTo(605, 215, duration = MOVE_DURATION)
    # pyautogui.moveTo(855, 675, duration = MOVE_DURATION)

if __name__ == "__main__":
    main()
