# cv2.cvtColor takes a numpy ndarray as an argument
import sys

from pynput import keyboard
from module.filter_items import filter_items


def on_press(key):
    if key == keyboard.Key.f11:
        sys.exit()
    if key == keyboard.Key.f12:
        filter_items()


def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys


def main():
    start_listener()


if __name__ == "__main__":
    main()
