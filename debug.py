

import math
import random
import time
from matplotlib import pyplot as plt
import numpy
import os
from client import check_if_at_follow_cap, check_if_on_profile_page, combine_duplicate_coords, fast_scroll_down, find_all_pixels, get_coords_of_follow_buttons, get_name_of_current_profile, get_to_followers_page, get_to_following_page, get_to_profile_page, orientate_edge_window, restart_twitter, screenshot, use_webpage_search

from configuration import load_user_settings
import pyautogui
import pygetwindow
from image_rec import coords_is_equal, find_references, get_first_location, pixel_is_equal

from logger import Logger
import subprocess
from database import Database


logger = Logger()
users_ive_followed_from_database= Database("users_ive_followed_from")
user_settings = load_user_settings()
launcher_path = user_settings["launcher_path"]

# orientate_edge_window(logger)

# plt.imshow(numpy.asarray(screenshot(region=[0,0,1400,2000])))
# plt.show()



