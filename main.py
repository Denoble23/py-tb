
import time
from matplotlib import pyplot as plt
import numpy
import pyautogui


from client import check_quit_key_press, click, click_list_of_follow_buttons, find_random_account_from_followers_list, get_coords_of_follow_buttons, get_name_of_current_profile, get_to_followers_page, get_to_following_page, get_to_notification_page, get_to_profile_page, look_for_unfollow_button_in_unfollow_page, orientate_twitter_window, restart_twitter, screenshot, search_region_for_pixel, use_webpage_search
from image_rec import check_for_location, find_references, pixel_is_equal
from logger import Logger

logger=Logger()

def detect_screen():
    orientate_twitter_window(logger)
    
    
def check_if_on_profile_page():
    check_quit_key_press()
    current_image = screenshot()
    reference_folder = "profile_page"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",

    ]
    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)


def check_if_somewhere_on_twitter_main():
    check_quit_key_press()
    current_image = screenshot()
    reference_folder = "somewhere_on_twitter_main"
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",

    ]
    locations = find_references(
        screenshot=current_image,
        folder=reference_folder,
        names=references,
        tolerance=0.97
    )
    return check_for_location(locations)


def check_if_on_following_page():
    on_main=check_if_somewhere_on_twitter_main()
    if not on_main:
        return False
    
    #get a screenshot of region
    region=[654,121,35,20]
    iar=numpy.asarray(screenshot(region=region))
    
    #define positive pix
    sentinel=[54,253,255]
    sentinel2=[29,155,240]
    
    #loop through every pix
    x_index=34
    while x_index>-1:
        y_index=19
        while y_index>-1:
            current_pix=iar[y_index][x_index]
            #if one of the pixels are positive return true
            
            if (pixel_is_equal(current_pix,sentinel,tol=15))or(pixel_is_equal(current_pix,sentinel2,tol=15)):
                return True
    
            y_index=y_index-1
        x_index=x_index-1
    
    #if we find no positive pixels return false
    return False


#intro
logger.log("Twitter follow bot")
restart_twitter(logger)
logger.log("Select mode")

#mode select
value = input("Select mode: \n [1]unfollow all mode \n [2]follow mode \n")
value=int(value)
logger.log(value)



#unfollow mode
if value == 1:
    logger.log("Selected unfollow mode.")
    
    #get to profile page
    get_to_profile_page(logger)
    time.sleep(1)
    
    #get to following page
    get_to_following_page(logger)
    time.sleep(1)
    
    #unfollow loop
    #while there are still more people to unfollow:
    keep_looping=True
    has_more_to_unfollow = True
    while keep_looping:
        while (has_more_to_unfollow):
            check_quit_key_press()
            #look for following button
            following_button_coords=look_for_unfollow_button_in_unfollow_page(logger)
            if following_button_coords is None:
                has_more_to_unfollow=False
            
            #click following button
            check_quit_key_press()
            if (following_button_coords is not None)and(has_more_to_unfollow):
                click(following_button_coords[0],following_button_coords[1])
                time.sleep(0.25)
                #click unfollow in the popup window
                check_quit_key_press()
                click(600,660)
                time.sleep(0.25)
                logger.add_unfollow()
            
        logger.log("No more unfollow buttons on the page. Refreshing.")
        pyautogui.press('f5')
        has_more_to_unfollow=True
        time.sleep(4)
        
        if look_for_unfollow_button_in_unfollow_page(logger) is None:
            has_more_to_unfollow=False
            keep_looping=False

#follow mode
if value == 2:
    logger.log("Selected follow mode.")
    
    while True:
        #get to profile page
        get_to_profile_page(logger)
        time.sleep(3)
        
        #get to list of my followers
        get_to_followers_page(logger)
        time.sleep(3)
        
        #get a account to spam follow
        find_random_account_from_followers_list(logger)
        
        #get to their followers page
        get_to_followers_page(logger)
        time.sleep(4)
        
        #get coords of follow buttons
        follow_button_list=get_coords_of_follow_buttons(logger)

        #click that set of coords
        click_list_of_follow_buttons(follow_button_list,logger)
        time.sleep(3)

