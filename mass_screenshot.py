
import pyautogui

from image_rec import screenshot

def screenshot_around_mouse():
    origin=pyautogui.position()
    
    region=[origin[0],origin[1],15,15]
    
    screenshot(region=region)
    
    path_to_save=r"C:\Users\Matt\Desktop\inc_pics"
    
    time=