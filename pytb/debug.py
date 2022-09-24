

from calendar import c
import time
from http.client import PROXY_AUTHENTICATION_REQUIRED

import numpy
import pyautogui
import pyperclip
from matplotlib import pyplot as plt

from pytb.client import (check_for_blacklist_in_text, check_quit_key_press, click,  find_all_pixels, get_name_of_current_profile,
                         get_this_profiles_bio_text, get_to_profile_page, get_to_random_account_from_followers_list, get_to_random_account_from_followers_list_with_blacklist, orientate_edge_window, screenshot, search_region_for_pixel, show_image, use_webpage_search)
from pytb.configuration import load_user_settings
from pytb.database import Database
from pytb.image_rec import (check_for_location, coords_is_equal,
                            find_references, get_first_location, pixel_is_equal)
from pytb.logger import Logger

logger = Logger()
users_ive_followed_from_database = Database("users_ive_followed_from")
user_settings = load_user_settings()
launcher_path = user_settings["launcher_path"]

# orientate_edge_window(logger)

# show_image(screenshot(region=[0,0,1400,2000]))


def get_to_following_page(logger):
    logger.log("Getting to this profile's following page")
    check_quit_key_press()
    
    coord=(find_following_page(logger))
    if coord is None: return "restart"
    pyautogui.moveTo(coord[0],coord[1],duration=0.33)
    time.sleep(0.2)
    pyautogui.click()
    time.sleep(1)

def find_following_page(logger):
    use_webpage_search('Following')
    
    color_orange=[253,151,60]
    color_yellow=[255,255,58]
    color_white=[255,255,255]

    # show_image(screenshot([100,500,250,150]))

    iar=numpy.asarray(screenshot())

    for x_coord in range(100,350):
        for y_coord in range(500,650):
            coord=[x_coord,y_coord]
            pixel=iar[y_coord][x_coord]
            if pixel_is_equal(pixel,color_yellow,tol=30): return coord
            if pixel_is_equal(pixel,color_orange,tol=30): return coord
            
            
       
    


