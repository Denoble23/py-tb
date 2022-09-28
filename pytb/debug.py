

import time
from http.client import PROXY_AUTHENTICATION_REQUIRED

import numpy
import pyautogui
import pyperclip
from matplotlib import pyplot as plt

from pytb.client import (
    check_for_blacklist_in_text, get_name_of_current_profile,
    get_this_profiles_bio_text, get_to_random_account_from_followers_list,
    get_to_random_account_from_followers_list_with_blacklist,
    orientate_edge_window, screenshot)
from pytb.configuration import load_user_settings
from pytb.database import Database
from pytb.image_rec import (check_for_location, coords_is_equal,
                            find_references, get_first_location,
                            pixel_is_equal)
from pytb.logger import Logger

logger = Logger()
users_ive_followed_from_database = Database("users_ive_followed_from")
user_settings = load_user_settings()
launcher_path = user_settings["launcher_path"]

# orientate_edge_window(logger)

# plt.imshow(numpy.asarray(screenshot(region=[0, 0, 1400, 2000])))
# plt.show()




