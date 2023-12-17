import pyautogui
from PIL import Image

def screenshot() -> Image:
    return pyautogui.screenshot()