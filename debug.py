

import random
import time
from matplotlib import pyplot as plt
import numpy
from client import check_if_on_profile_page, click, find_all_pixels, get_to_followers_page, get_to_following_page, orientate_twitter_window, screenshot, unfollow_from_following_page, use_webpage_search


from logger import Logger
from database import Database


logger=Logger()
users_ive_followed_from_database= Database("users_ive_followed_from")



# orientate_twitter_window(logger)

# plt.imshow(numpy.asarray(screenshot()))
# plt.show()

get_to_following_page(logger)

