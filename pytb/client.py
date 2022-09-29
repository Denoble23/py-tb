import math
import random
import subprocess
import sys
import time

import keyboard
import numpy
import pyautogui
import pygetwindow
import pyperclip
from matplotlib import pyplot as plt
from screeninfo import get_monitors

from pytb.image_rec import (check_for_location, coords_is_equal,
                            find_references, get_first_location,
                            pixel_is_equal)


def scroll_down():
    #click twitter window
    pyautogui.click(40,888,clicks=3,interval=0.05)
    time.sleep(0.05)
    check_quit_key_press()

    time.sleep(0.5)
    pyautogui.press('pagedown')


def scroll_up():
    #click twitter window
    pyautogui.click(20,888,clicks=3,interval=0.05)
    time.sleep(0.05)
    check_quit_key_press()

    time.sleep(0.5)
    pyautogui.press('pageup')


def click(x, y, clicks=1, interval=0.0,duration=0.33,move_to_original_position=False):
    original_pos = pyautogui.position()
    loops = 0
    pyautogui.moveTo(x,y,duration=duration)
    while loops < clicks:
        check_quit_key_press()
        pyautogui.click(x=x, y=y)
        loops = loops + 1
        time.sleep(interval)
    if move_to_original_position:
            pyautogui.moveTo(original_pos[0], original_pos[1])


def check_quit_key_press():
    if keyboard.is_pressed("space"):
        print("Space is held. Quitting the program")
        sys.exit()
    if keyboard.is_pressed("pause"):
        print("Pausing program until pause is held again")
        time.sleep(5)
        pressed=False
        while not(pressed):
            time.sleep(0.05)
            if keyboard.is_pressed("pause"):
                print("Pause held again. Resuming program.")
                pressed=True


def screenshot(region=(0, 0, 1600, 1600)):
    if region is None:
        return pyautogui.screenshot()
    else:
        return pyautogui.screenshot(region=region)


def orientate_edge_window(logger):
    logger.log('Looking for window')

    edge_window = pygetwindow.getWindowsWithTitle(
        "edge")[0]
    time.sleep(1)


    logger.log('Minimizing')
    edge_window.minimize()
    logger.log('Restoring')
    edge_window.restore()
    edge_window.restore()

    time.sleep(1)

    logger.log('Moving to topleft')
    edge_window.moveTo(0, 0)
    time.sleep(1)

    logger.log('Setting size.')
    edge_window.resizeTo(1200, 1000) # set size to 100x100
    time.sleep(1)

    handle_edge_restore_notification(logger)


def check_for_restore_logo():
    iar=numpy.asarray(screenshot())
    pix_list=[]
    pix_list.append(iar[156][1102])
    pix_list.append(iar[172][1104])
    pix_list.append(iar[175][1160])
    pix_list.append(iar[158][1158])

    sentinel=[0,120,212]
    for pix in pix_list:
        if not(pixel_is_equal(pix,sentinel,tol=35)): return False
    return True


def handle_edge_restore_notification(logger):
    if check_for_restore_logo():
        logger.log("Handling edge's 'restore pages' notification.")
        origin=pyautogui.position()
        pyautogui.moveTo(1167,88,duration=0.33)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(origin[0],origin[1],duration=0.33)


def open_twitter_in_edge(logger):
    logger.log("Opening twitter from edge main.")
    #click search bar of edge
    click(200,62)
    time.sleep(0.2)

    #type out twitter.com
    pyautogui.typewrite("twitter.com",interval=0.01)
    time.sleep(1)
    pyautogui.click(188,99)
    time.sleep(3)

    handle_edge_restore_notification(logger)


def restart_twitter(logger, launcher_path):
    edge_window=pygetwindow.getWindowsWithTitle("edge")
    if len(edge_window)==0:
        logger.log("edge not found. opening edge.")
        #open edge
        subprocess.Popen(launcher_path)
        time.sleep(2)

        #orientate twitter
        orientate_edge_window(logger)
        time.sleep(2)

        #open twitter
        open_twitter_in_edge(logger)
        time.sleep(2)

    else:
        #close existing edge
        edge_window=edge_window[0]
        logger.log("Found edge open. Closing it.")
        edge_window.close()
        time.sleep(3)

        #reopen edge
        logger.log("Reopening edge.")
        subprocess.Popen(launcher_path)
        time.sleep(3)

        #orientate edge
        orientate_edge_window(logger)

        #open twitter
        open_twitter_in_edge(logger)


def get_to_profile_page(logger):
    logger.log("Getting to profile page.")
    check_quit_key_press()

    #click profile icon on the left side
    logger.log('Clicking profile page')

    click(93,517)
    time.sleep(1)

    if not(check_if_on_profile_page()):
        logger.log("Failed to get to profile page.")
        return "restart"

    logger.log("Made it to profile page.")



def get_to_following_page(logger):
    logger.log("Getting to this profile's following page")
    check_quit_key_press()
    
    coord=(find_following_page(logger))
    if coord is None: return "restart"
    pyautogui.moveTo(coord[0],coord[1],duration=0.33)
    time.sleep(1)
    pyautogui.click()

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
            
            
       

def show_image(image):
    plt.imshow(numpy.asarray(image))
    plt.show()

def check_if_on_profile_page():
    use_webpage_search('edit profile')
    iar=numpy.asarray(screenshot())
    pix_list=[
    iar[355][639],
    iar[367][666],
    iar[354][636],
    ]
    color_orange=[255,151,60]
    for pix in pix_list:
        if not(pixel_is_equal(pix,color_orange,tol=30)): return False
    return True
    
    


def check_if_on_twitter_main():
    references = [
        "1.png",
        "2.png",
        "3.png",
    ]

    locations = find_references(
        screenshot=screenshot(),
        folder="somewhere_on_twitter_main",
        names=references,
        tolerance=0.97
    )

    return check_for_location(locations)


def find_following_button():
    use_webpage_search('following')

    color_yellow=[255,255,0]
    region=[650,140,35,845]

    coord_list=find_all_pixels(region,color_yellow,tolerance=10)
    if len(coord_list)==0:
        return None

    return coord_list[0]


def look_for_unfollow_button_in_unfollow_page():
    use_webpage_search('following')

    #loop through all the coords top down looking for yellow pixels.
    #make screenshot
    #logger.log("Looking at the page for highlighted unfollow buttons.")
    iar=numpy.asarray(screenshot())

    #close search function
    pyautogui.click(997,51,clicks=3,interval=0.1)
    check_quit_key_press()

    coords=[731,137]
    #loop
    while coords[1] < 1085:
        #assess current pixel
        current_pix=iar[coords[1]][coords[0]]
        sentinel=[255,255,0]
        if pixel_is_equal(sentinel,current_pix,tol=15):
            #logger.log(f"Unfollow coord found at {coords}.")
            return coords
        check_quit_key_press()

        #increment y coord by 1
        coords=[coords[0],coords[1]+1]
        check_quit_key_press()

    return None


def use_webpage_search(search_string):
    #click twitter window
    pyautogui.click(40,888,clicks=3,interval=0.05)
    time.sleep(0.05)
    check_quit_key_press()

    #open search function
    #logger.log("Opening webpage search function")
    pyautogui.keyDown('ctrl')
    time.sleep(0.05)
    pyautogui.press('f')
    time.sleep(0.05)
    pyautogui.keyUp('ctrl')
    time.sleep(0.05)
    check_quit_key_press()

    #type 'following' into ctrl+f search function
    #logger.log("Searching for 'following.' ")
    pyautogui.typewrite(search_string,interval=0.01)
    check_quit_key_press()
    time.sleep(1)


def search_region_for_pixel(region,color):
    #searches entire region for pixel and returns first coords it finds

    #make image-as-array
    iar=numpy.asarray(screenshot())


    x_coord=region[0]
    while x_coord<(region[0]+region[2]):
        y_coord=region[1]
        while y_coord<(region[1]+region[3]):
            #for each pixel in region
            current_pix=iar[x_coord][y_coord]

            #print(f"Current coord: {x_coord},{y_coord}|Current pix: {current_pix}")

            sentinel=color
            if pixel_is_equal(current_pix,sentinel,tol=15):
                return [y_coord,x_coord]
            y_coord=y_coord+1
        x_coord=x_coord+1

    return None


def find_all_pixels(region,color,tolerance=25):
    #### LOGIC FOR MAKING FOR_ALL_PIXEL() METHOD VARIABLES
    x_limit=(region[0])+(region[2])
    y_limit=(region[1])+(region[3])
    x_start=region[0]
    y_start=region[1]

    #### CHECK FOR REGION LOGIC
    # print(f"x_limit is {x_limit}")
    # print(f"y_limit is {y_limit}")
    # print(f"x_start is {x_start}")
    # print(f"y_start is {y_start}")

    #get iar
    iar=numpy.asarray(screenshot())

    #list for return
    coords_list=[]

    x_coord=x_start
    while x_coord<x_limit:
        y_coord=y_start
        while y_coord<y_limit:
        #for each coord
            #get current coord
            curernt_coord=[x_coord,y_coord]

            #get current pixel
            current_pix=iar[y_coord][x_coord]

            #if pixel is close enough to add add it
            if pixel_is_equal(current_pix,color,tol=tolerance):
                coords_list.append(curernt_coord)

            #increment
            y_coord=y_coord+1
        x_coord=x_coord+1

    return coords_list


def get_to_followers_page(logger):
    logger.log("Getting to this profile's followers page")
    coord = find_followers_page()
    
    if coord is None: return "restart"

    pyautogui.moveTo(coord[0],coord[1],duration=0.33)
    time.sleep(0.33)
    pyautogui.click()
    time.sleep(1)


def find_followers_page():
    use_webpage_search('Followers')
    
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


def combine_duplicate_coords(coords_list,tol=50):
    #method will take an array of coords ([x,y]) and combine duplicates according to a certain tolerance.

    new_coords_list=[]

    #loop vars
    total_coords_in_list=len(coords_list)
    index=0

    #loop through every coord in coords_list
    while index<total_coords_in_list:
        #get current coord
        current_coord=coords_list[index]

        #if current_coord doesnt exist in new_coords_list make new coord in new coords list
        if not(check_if_coord_in_coord_list(current_coord,new_coords_list,tol=tol)):
            new_coords_list.append(current_coord)

        #increment
        index=index+1

    return new_coords_list


def check_if_coord_in_coord_list(coord,coord_list,tol=50):
    #loop vars
    index=0
    total_coords_in_coords_list=len(coord_list)

    while index<total_coords_in_coords_list:

        #get curent coord
        current_coord=coord_list[index]


        #compare current coord with coord in question
        if coords_is_equal(current_coord,coord,tol):
            return True

        #increment
        index=index+1

    #if we make it out of the loop without ever returning True then that means the coord is unique
    return False


def fast_scroll_down():
    #pixel vars
    color_grey=[193,193,193]
    region=[1130,103,5,1050]

    #get grey coordslist
    coords_list=find_all_pixels(region,color_grey)

    #handle no coord found
    if (coords_list is None)or(coords_list==[]):
        return "restart"

    #get coord
    coord=coords_list[0]
    coord[1]=coord[1]+10

    #move to grey bar
    pyautogui.moveTo(coord[0],coord[1],duration=0.2)
    time.sleep(0.2)

    #scroll it down
    pyautogui.dragTo(1182,1155,duration=0.3)


def randomly_scroll_down(logger,scroll_limit=7):
    scrolls=random.randint(0,scroll_limit)
    while scrolls>0:
        check_quit_key_press()
        logger.log(f"Scrolling: {scrolls}")

        if random.randint(1,2)==1:
            fast_scroll_down()
            time.sleep(1)
        else:
            scroll_down()
            time.sleep(1)


        scrolls=scrolls-1


def get_to_random_account_from_followers_list_with_blacklist(logger,users_ive_followed_from_database):
    # get to profile page
    if get_to_profile_page(logger) == "restart":
        return "restart"
    time.sleep(1)

    # get to list of my followers
    if get_to_followers_page(logger) == "restart":
        return "restart"
    time.sleep(1)
    
    #randomly scroll
    logger.log("Randomly scrolling.")
    randomly_scroll_down(logger)

    #click account
    logger.log("Clicking chosen random account.")
    x_coord=187
    y_coord=random.randint(190,925)
    coord=[x_coord,y_coord]
    click(coord[0],coord[1])
    check_quit_key_press()
    time.sleep(1)


    #get name of current guy
    name=get_name_of_current_profile()
    logger.log(f"This profile's name is [{name}]")
    time.sleep(1)

    #check if name in file
    if users_ive_followed_from_database.check_if_user_in_users_followed_database(name):
        logger.log("This account has been targetted before. Redoing search algorithm.")
        logger.log("Skipping this profile and recalling this method.")
        get_to_random_account_from_followers_list_with_blacklist(logger,users_ive_followed_from_database)
    logger.log("1. This name passed database check.")
    time.sleep(1)
    
    #check if this name contains blacklist strings
    name_check=(check_for_blacklist_in_text(name))
    if name_check != "pass":
        logger.log(f"The name [{name}] failed blacklist check with string [{name_check}]")
        logger.log("Skipping this profile and recalling this method.")
        users_ive_followed_from_database.add_username_to_database(name)
        get_to_random_account_from_followers_list_with_blacklist(logger,users_ive_followed_from_database)
    logger.log("2. This name passed blacklist check.")
    time.sleep(1)
    
    
    #check if this profile's bio contains blacklist strings
    bio_text=get_this_profiles_bio_text()
    bio_check=check_for_blacklist_in_text(bio_text)
    if bio_check != "pass":
        logger.log(f"This bio failed the blacklist check with string [{bio_check}]")
        logger.log("Skipping this profile and recalling this method.")
        #write this name to db so we dont have to check again
        users_ive_followed_from_database.add_username_to_database(name)
        #call this method again
        get_to_random_account_from_followers_list_with_blacklist(logger,users_ive_followed_from_database)
    logger.log("3. This bio passed blacklist check.")
    time.sleep(1)
    
    #if the name isnt in the file, add this name to the file, then return.
    logger.log("Verified that the chosen account is satisfactory. Writing this username to the database.")
    users_ive_followed_from_database.add_username_to_database(name)


def get_to_random_account_from_followers_list(logger):
    #starts on followers list page, ends on the page of a random follower
    
    #randomly scroll
    logger.log("Randomly scrolling.")
    randomly_scroll_down(logger,scroll_limit=20)

    #target account
    logger.log("Clicking chosen random account.")
    x_coord=187
    y_coord=random.randint(190,1142)
    coord=[x_coord,y_coord]
    click(coord[0],coord[1])
    check_quit_key_press()
    
    
def get_this_profiles_bio_text():
    #close dm tab
    close_messages_tab()
    
    #click open space
    pyautogui.click(190,450)
    
    #select region of bio
    # pyautogui.moveTo(118,471)
    # pyautogui.dragTo(610,659,duration=0.33)
    ####select all
    pyautogui.keyDown('ctrl')
    time.sleep(0.2)
    pyautogui.press('a')
    time.sleep(0.2)
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)
    
    time.sleep(0.2)
    #copy it
    pyautogui.keyDown('ctrl')
    time.sleep(0.2)
    pyautogui.press('c')
    time.sleep(0.2)
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)
    
    text= pyperclip.paste()
    
    #cut text to char count
    shortened_text=""
    index=000
    while index<500:
        shortened_text=shortened_text+text[index]
        index=index+1
        
    return shortened_text
        
        
def check_for_blacklist_in_text(text):
    #essentially blacklists any accounts having to do with sports, anime, onlyfans, youngboy, or anything promotional (like premium snap, dm fees, artists looking for comissions)
    blacklist=[
    "DubNation"
    ,"DUBNATION"
    ,"dubnation"
    ,"NBA"
    ,"nba"
    ,"Nba"
    ,"broke"
    ,"Broke"
    ,"youngboy" 
    ,"YoungBoy" 
    ,"YoungBoy Never Broke Again"
    ,"never nroke again"
    ,"Never nroke again"
    ,"Kentrell"
    ,"Rapper" 
    ,"YOUNG" 
    ,"BETTER" 
    ,"BROKE" 
    ,"NEVER" 
    ,"AGAIN" 
    ,"YOUNGBOY"
    ,"BLOCK" 
    ,"UNFOLLOW="
    ,"unfollow="
    ,"ratio" 
    ,"RATIO" 
    ,"I Own You"
    ,"i own you"
    ,"I own you"
    ,"I OWN YOU"
    ,"an L"
    ,"AN L"
    ,"TOP9"
    ,"TOP1"
    ,"TOP2"
    ,"TOP3"
    ,"TOP4"
    ,"TOP5"
    ,"TOP6"
    ,"TOP7"
    ,"TOP8"
    ,"onlyfans"
    ,"OF" 
    ,"ONLYFANS"
    ,"free" 
    ,"FREE" 
    ,"I follow back"
    ,"I fb" 
    ,"block" 
    ,"notis" 
    ,"christ" 
    ,"jesus"
    ,"Jesus"
    ,"manga"
    ,"anime"
    ,"promo"
    ,"dm me for"
    ,"Dm Fee" 
    ,"DM fee" 
    ,"dm fee" 
    ,"DM FEE" 
    ,"DM ME"
    ,"DM me"
    ,"dm me"
    ,"Dm me"
    ,"cosplay" 
    ,"FOLLOW BACK"
    ,"follow back"
    ,"L's",
    "ratio",
    "Ratio",
    "RATIO",
    
    ]
    
    for string in blacklist:
        if string in text:
            print("Failed blacklist check with string: [",string,"]")
            return string
    
    return 'pass'


def check_if_name_is_in_file(name,file):
    Lines=file.readlines()
    for line in Lines:
        if line.startswith(name):
            return True
    return False


def get_name_of_current_profile():
    #click coord and copy name
    pyautogui.moveTo(150,450,duration=0.2)
    pyautogui.click(clicks=2,interval=0.2)
    time.sleep(0.2)
    pyautogui.keyDown('ctrl')
    time.sleep(0.2)
    pyautogui.press('c')
    time.sleep(0.2)
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)

    #get name from clipboard
    return pyperclip.paste()


def get_coords_of_follow_buttons(logger):
    #make iar
    iar=numpy.asarray(screenshot())

    #search for follow
    use_webpage_search('follow')

    #find all yellow coords in the vertical strip (686,226)->(686,1089)
    color_yellow=[255,255,0]

    yellow_pix_list=[]
    for y_coord in range(226,1089):
        currentpix=iar[y_coord][686]
        if pixel_is_equal(color_yellow,currentpix,tol=5):
            yellow_pix_list.append([686,y_coord])

    return combine_duplicate_coords(yellow_pix_list)


def click_list_of_follow_buttons(follow_button_list,logger):
    length=len(follow_button_list)
    logger.log(f"Clicking the follow buttons that were given. I have {length} coords")
    index=0
    while index<length:
        check_quit_key_press()
        current_coord=follow_button_list[index]
        if (random . randint(1, 3) != 1)or(len(follow_button_list)<5):
            logger.log("Followed one.")
            click(current_coord[0],current_coord[1])
            logger.add_follow()
            click(20,900)
        time.sleep(0.05)

        index+=1

    #check if throttled
    logger.log("Checking if follow throttle message has appeared this go-around.")
    if check_if_at_follow_cap():
        #remove a follow count for each one that was wrongly added to count
        length=math.floor((len(follow_button_list))*0.66)
        index=0
        logger.log(f"Removing {length} follows from follow count.")
        while index<length:
            logger.remove_follow()
            index=index+1

        return "throttled"


def unfollow_from_following_page(logger):
    check_quit_key_press()
    has_more_to_unfollow=True
    while has_more_to_unfollow:
        #find coord of unfollow
        following_button_coords = look_for_unfollow_button_in_unfollow_page()

        #unfollow if given a coord
        if following_button_coords is not None:
            check_quit_key_press()
            #click unfollow button
            click(following_button_coords[0],following_button_coords[1])
            time.sleep(0.33)
            #click unfollow button in resulting popup
            click(600, 660)
            time.sleep(0.33)
        else:
            check_quit_key_press()
            pyautogui.press('f5')
            time.sleep(2.5)

        #check if has_more_to_unfollow
        check_quit_key_press()
        if look_for_unfollow_button_in_unfollow_page() is None:
            has_more_to_unfollow=False


def check_if_at_follow_cap():
    use_webpage_search("You are unable")
    color_orange=[255,150,50]
    region=[395,1135,200,10]
    coords_list=find_all_pixels(region,color_orange,tolerance=10)

    scroll_up()

    if (coords_list is None)or(coords_list ==[]):
        return False
    return True


def check_for_restore_pages_notification():
    iar=numpy.asarray(screenshot())

    pix1=iar[115][1117]
    pix2=iar[175][1100]
    pix3=iar[158][1139]

    color_blue=[0,120,212]

    if not(pixel_is_equal(pix1,color_blue,tol=15)):
        return False
    if not(pixel_is_equal(pix2,color_blue,tol=15)):
        return False
    if not(pixel_is_equal(pix3,color_blue,tol=15)):
        return False
    return True


def find_follow_buttons():
    check_quit_key_press()

    #search for follow
    use_webpage_search('follow')
    time.sleep(1)

    #make iar
    iar=numpy.asarray(screenshot())

    coord_list=[]
    x_coord=662
    sentinel=[255,255,0]
    for y_coord in range(202,1120):
        current_pixel=iar[y_coord][x_coord]
        current_coord=[x_coord,y_coord]
        if (y_coord % 10 == 0)and(pixel_is_equal(current_pixel,sentinel,tol=25)):
            coord_list.append(current_coord)

    return coord_list


def get_screen_resolution():
    monitor_1=get_monitors()[0]
    w=monitor_1.width
    h=monitor_1.height
    return [w,h]


def orientate_terminal():
    try:
        terminal_window = pygetwindow.getWindowsWithTitle(
            "py-tb v")[0]
        terminal_window.minimize()
        terminal_window.restore()

        #resize according to monitor width
        monitor_width=get_screen_resolution()[0]
        terminal_width=monitor_width-1290
        terminal_window.resizeTo(terminal_width, 350)

        #move window
        terminal_window.moveTo(970,5)

        terminal_window.moveTo(1285, 5)
    except BaseException:
        print("Couldn't orientate terminal.")


def close_messages_tab():
    if check_if_messages_tab_is_open():
        print("closing messages tab")
        pyautogui.moveTo(1057,688,duration=0.33)
        time.sleep(0.33)
        pyautogui.click()
        time.sleep(0.33)


def check_if_messages_tab_is_open():
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
    ]

    locations = find_references(
        screenshot=screenshot(),
        folder="find_messages_tab",
        names=references,
        tolerance=0.97
    )

    return check_for_location(locations)
    
    
def find_more_profile_actions_button():
    references = [
        "1.png",
        "2.png",
        "3.png",
    ]

    locations = find_references(
        screenshot=screenshot(),
        folder="find_more_profile_actions_button",
        names=references,
        tolerance=0.97
    )

    coords= get_first_location(locations)
    return [coords[1],coords[0]]


def find_block_button():
    references = [
        "1.png",
        "2.png",
        "3.png",
        "4.png",
        "5.png",
        
    ]

    locations = find_references(
        screenshot=screenshot(),
        folder="find_block_button",
        names=references,
        tolerance=0.97
    )

    coords= get_first_location(locations)
    return [coords[1],coords[0]]


def block_this_profile(logger):
    #click three dots on this profile
    logger.log("Opening the more actions tab for this profile.")
    more_actions_button_coords=find_more_profile_actions_button()
    pyautogui.moveTo(more_actions_button_coords[0],more_actions_button_coords[1],duration=0.33)
    time.sleep(0.33)
    pyautogui.click()
    time.sleep(2)
    
    #click block
    logger.log("Clicking block button from list of more profile actions.")
    block_button_coords=find_block_button()
    pyautogui.moveTo(block_button_coords[0],block_button_coords[1],duration=0.33)
    time.sleep(0.33)
    pyautogui.click()
    time.sleep(2)
    
    #click confirm block
    logger.log("Clicking red block button to confirm block.")
    confirm_block_button_coords=[567,673]
    pyautogui.moveTo(confirm_block_button_coords[0],confirm_block_button_coords[1],duration=0.33)
    time.sleep(0.33)
    pyautogui.click()
    time.sleep(1)
    
    




