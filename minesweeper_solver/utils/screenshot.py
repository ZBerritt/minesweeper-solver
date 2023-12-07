import pyautogui
from PIL import Image

# TODO: Possibly find a faster library for screenshotting
def screenshot() -> Image:
    return pyautogui.screenshot()