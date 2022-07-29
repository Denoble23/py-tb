
import time
from matplotlib import pyplot as plt
import numpy
import pyautogui


from client import check_quit_key_press, click, click_list_of_follow_buttons, find_random_account_from_followers_list, get_coords_of_follow_buttons, get_name_of_current_profile, get_to_followers_page, get_to_following_page, get_to_notification_page, get_to_profile_page, look_for_unfollow_button_in_unfollow_page, orientate_twitter_window, restart_twitter, screenshot, search_region_for_pixel, use_webpage_search
from configuration import load_user_settings
from database import Database
from image_rec import check_for_location, find_references, pixel_is_equal
from logger import Logger

logger = Logger()
users_ive_followed_from_database= Database("users_ive_followed_from")
user_settings = load_user_settings()
launcher_path = user_settings["launcher_path"]
mode=0
state=""

def main():
    # intro
    

    # unfollow mode
    if value == 1:
        logger.log("Selected unfollow mode.")

        # get to profile page
        get_to_profile_page(logger)
        time.sleep(1)

        # get to following page
        get_to_following_page(logger)
        time.sleep(1)

        # unfollow loop
        # while there are still more people to unfollow:
        keep_looping = True
        has_more_to_unfollow = True
        while keep_looping:
            while (has_more_to_unfollow):
                check_quit_key_press()
                # look for following button
                following_button_coords = look_for_unfollow_button_in_unfollow_page(
                    logger)
                if following_button_coords is None:
                    has_more_to_unfollow = False

                # click following button
                check_quit_key_press()
                if (following_button_coords is not None) and (has_more_to_unfollow):
                    click(following_button_coords[0],
                          following_button_coords[1])
                    time.sleep(0.25)
                    # click unfollow in the popup window
                    check_quit_key_press()
                    click(600, 660)
                    time.sleep(0.25)
                    logger.add_unfollow()

            logger.log("No more unfollow buttons on the page. Refreshing.")
            pyautogui.press('f5')
            has_more_to_unfollow = True
            time.sleep(4)

            if look_for_unfollow_button_in_unfollow_page(logger) is None:
                has_more_to_unfollow = False
                keep_looping = False

    # follow mode
    if value == 2:
        logger.log("Selected follow mode.")

        while True:
            # get to profile page
            get_to_profile_page(logger)
            time.sleep(3)

            # get to list of my followers
            get_to_followers_page(logger)
            time.sleep(3)

            # get a account to spam follow
            find_random_account_from_followers_list(logger,users_ive_followed_from_database)

            # get to their followers page
            if get_to_followers_page(logger) != "coord_not_found":
                time.sleep(4)

                # get coords of follow buttons
                follow_button_list = get_coords_of_follow_buttons(logger)

                # click that set of coords
                click_list_of_follow_buttons(follow_button_list, logger)
                time.sleep(3)
            else:
                logger.log("Had trouble locating the followers button on this profile. Skipping this profile.")


def main_loops():
    if state=="restart":
        state_restart()
    if state=="intro":
        pass
    if state=="unfollow_mode":
        pass
    if state=="follow_mode":
        pass
    
        

def state_restart():
    restart_twitter(restart_twitter(logger, launcher_path))
    if mode ==0:
        return "intro"
    if mode ==1:
        return "unfollow_mode"
    if mode ==2:
        return "follow_mode"
    

def state_intro():
    logger.log("Select mode")

    # mode select
    value = input("Select mode: \n [1]unfollow all mode \n [2]follow mode \n")
    value = int(value)
    logger.log(value)

def state_unfollow_mode():
    pass

def state_follow_mode():
    pass





if __name__ == "__main__":
    main()