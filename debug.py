

from matplotlib import pyplot as plt
import numpy
from client import click_list_of_follow_buttons, combine_duplicate_coords, find_all_pixels, get_coords_of_follow_buttons, get_name_of_current_profile, get_to_followers_page, orientate_twitter_window, screenshot
from database import check_if_user_in_users_followed_database
from image_rec import pixel_is_equal

from logger import Logger


logger=Logger()

# orientate_twitter_window(logger)

# plt.imshow(numpy.asarray(screenshot()))
# plt.show()


print(check_if_user_in_users_followed_database(name))