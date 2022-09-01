
import time
from matplotlib import pyplot as plt
import numpy
import pyautogui


from client import check_quit_key_press, click, click_list_of_follow_buttons, find_follow_buttons, find_following_button, find_random_account_from_followers_list, get_coords_of_follow_buttons, get_name_of_current_profile, get_to_followers_page, get_to_following_page,  get_to_profile_page, look_for_unfollow_button_in_unfollow_page, orientate_edge_window, restart_twitter, screenshot, scroll_down, search_region_for_pixel, use_webpage_search
from configuration import load_user_settings
from database import Database
from image_rec import check_for_location, find_references, pixel_is_equal
from logger import Logger

logger = Logger()
users_ive_followed_from_database= Database("users_ive_followed_from")
user_settings = load_user_settings()
launcher_path = user_settings["launcher_path"]



def main():
    state="restart"
    
    mode=0
    while True:
        logger.log(f"---------CURRENT STATE IS {state}---------")
        
        if state=="restart":
            state=state_restart(mode)
        if state=="intro":
            logger.log("-----STATE=intro")
            logger.log("Select mode")
            # mode select
            value = input("Select mode: \n [1]unfollow all mode \n [2]follow mode \n")
            value = int(value)
            logger.log(value)
            mode=value
            if mode ==0:
                state= "intro"
            if mode ==1:
                state= "unfollow_mode"
            if mode ==2:
                state= "follow_mode"
        if state=="unfollow_mode":
            state=state_unfollow_mode()
        if state=="follow_mode":
            state=state_follow_mode()
        if state=="throttled":
            state=state_throttled(mode)
        
        if mode ==0:
            state= "intro"
        if mode ==1:
            state= "unfollow_mode"
        if mode ==2:
            state= "follow_mode"


def state_throttled(mode):
    logger.log("Bot is unable to follow more right now. Waiting 5 minutes.")
    loops=300
    while loops>0:
        check_quit_key_press()
        logger.log(f"Waiting {loops} seconds more.")
        time.sleep(1)
        loops=loops-1
    if mode ==0:
        return "intro"
    if mode ==1:
        return "unfollow_mode"
    if mode ==2:
        return "follow_mode"


def state_restart(mode):
    logger.add_restart()
    logger.log("-----STATE=restart")
    restart_twitter(logger, launcher_path)
    if mode ==0:
        return "intro"
    if mode ==1:
        return "unfollow_mode"
    if mode ==2:
        return "follow_mode"
    

def state_unfollow_mode():
    logger.log("-----STATE=unfollow_mode")
    
    # get to profile page
    if get_to_profile_page(logger)=="restart":
        return "restart"
    time.sleep(0.33)

    # get to following page
    if get_to_following_page(logger)=="restart":
        return "restart"
    time.sleep(1)
  
    has_more_to_unfollow=True
    while has_more_to_unfollow:
        has_coords=True
        while has_coords:
            following_button_coord=find_following_button()
            if following_button_coord is None:
                has_coords = False
            else:
                #click 'following' button
                pyautogui.click(x=following_button_coord[0],y=following_button_coord[1],duration=0.33)
                time.sleep(0.33)
                
                #click 'unfollow' button
                pyautogui.click(597,667,duration=0.33)
                
                #add to logger
                logger.add_unfollow()
                
                logger.log("Unfollowed.")
        
        #when u run out of coords on screen
        pyautogui.press("f5")
        time.sleep(3)
        
        #if screen has no followwing buttons then we're done unfollowing
        if find_following_button() is None:
            has_more_to_unfollow=False
        

def state_follow_mode():
    logger.log("-----STATE=follow_mode")
    while True:
        # get to profile page
        if get_to_profile_page(logger)=="restart":
            return "restart"
        time.sleep(0.33)

        # get to list of my followers
        if get_to_followers_page(logger)=="restart":
            return "restart"
        time.sleep(1)

        # get a account to spam follow
        find_random_account_from_followers_list(logger,users_ive_followed_from_database)
        time.sleep(0.33)

        # get to their followers page
        if get_to_followers_page(logger) != "coord_not_found":
            # get coords of follow buttons
            follow_button_list = find_follow_buttons()

            # click that set of coords
            if click_list_of_follow_buttons(follow_button_list, logger)=="throttled":
                return "throttled"
            time.sleep(0.33)
        
            #scroll for next loop
            scroll_down()

            # get coords of follow buttons
            follow_button_list = find_follow_buttons()

            # click that set of coords
            if click_list_of_follow_buttons(follow_button_list, logger)=="throttled":
                return "throttled"
            time.sleep(0.33)
        else:
            logger.log("Had trouble locating the followers button on this profile. Skipping this profile.")


if __name__ == "__main__":
    main()