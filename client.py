import math
import random
import subprocess
import sys
import time
from unittest.mock import sentinel
import keyboard
from matplotlib import pyplot as plt
import numpy
import pyautogui
import pygetwindow
import os
import pyperclip

from image_rec import check_for_location, coords_is_equal, find_references, pixel_is_equal


def scroll_down():
    #click twitter window
    pyautogui.click(137,888,clicks=3,interval=0.05)
    time.sleep(0.05)
    check_quit_key_press()
    
    time.sleep(0.5)
    pyautogui.press('pagedown')


def scroll_up():
    #click twitter window
    pyautogui.click(137,888,clicks=3,interval=0.05)
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
    edge_window.resizeTo(1200, 1200) # set size to 100x100
    time.sleep(1)
    
    handle_restore_pages_notification(logger)


def open_twitter_in_edge(logger):
    logger.log("Opening twitter from edge main.")
    #click search bar of edge
    click(200,62)
    time.sleep(0.2)
    
    #type out twitter.com
    pyautogui.typewrite("twitter.com",interval=0.01)
    pyautogui.press('enter')
    time.sleep(3)


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
    click(93,517,clicks=3,interval=0.2)
    time.sleep(2)
    on_profile= check_if_on_profile_page()
    if not(on_profile):
        return "restart"
    if not(check_if_on_profile_page()):
        return "restart"
    logger.log("Made it to profile page.")
    
    
def check_if_on_profile_page():
    use_webpage_search('edit profile')
    region=[640,350,25,25]
    color=[255,150,50]
    coords_list=find_all_pixels(region,color,tolerance=10)
    if (coords_list is not None)and(coords_list != []):
        return True
    return False
    
    
def get_to_following_page(logger):
    logger.log("Getting to this profile's following page")
    check_quit_key_press()
    use_webpage_search("following")
    
    region=[160,525,125,135]
    color_orange=[255,150,50]
    coords_list=find_all_pixels(region,color_orange,tolerance=5)
   
    if (coords_list is None)or(coords_list == []):
        return "restart"
    else:
        coord=coords_list[0]
        click(coord[0],coord[1],clicks=1)
    
    
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
    
    
def verify_following_button(coord):
    #get screenshot of region around selected coord
    region=[]
    iar=numpy.asarray(screenshot(region))
    
    #vars to loop through entire iar
    x_limit=999
    y_limit=999
    x_start=999
    y_start=999
    
    #VARS to collect total amount of yellow pixels around
    color_yellow=[255,255,0]
    total_positive_pixels=0
    
    x_coord=x_start
    while x_coord<x_limit:
        y_coord=y_start
        while y_coord<y_limit:
        #for each pixel in iar
            current_pix=iar[y_coord][x_coord]

        
        #increment
            y_coord=y_coord+1
        x_coord=x_coord+1


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
        
        
def get_to_notification_page(logger):
    #check if on profile page
    logger.log("Checking if we're on the twitter main page.")
    if not(check_if_on_twitter_main()):
        logger.log("We're not somewhere on the twitter main page.")
        return
    else:
        logger.log("We're somewhere on the twitter main page.")
    
    logger.log("Getting to notification page.")
    click(110,215)
    

def use_webpage_search(search_string):
    #click twitter window
    pyautogui.click(137,888,clicks=3,interval=0.05)
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
    
    
def look_for_someone_followed_me_in_notifications():
    use_webpage_search('followed you')
    
    
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
    check_quit_key_press()
    use_webpage_search("Followers")
    
    region=[154,421,311,200]
    color=[255,150,50]
    coords_list=find_all_pixels(region,color,tolerance=10)
   
    if (coords_list is None)or(coords_list == []):
        return "restart"
    else:
        coord=coords_list[0]
        click(coord[0],coord[1],clicks=1)
    

def find_followers_button_on_profile_to_follow_from():
    #search for following
    use_webpage_search('Following')
    
    #search for orange pixel
    region=[252,275,550,70]
    color=[255,150,50]
    return search_region_for_pixel(region,color)
    
   
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
    region=[1180,103,5,1050]
    
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
    

def randomly_scroll_down(logger):
    scrolls=random.randint(0,7)
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


def find_random_account_from_followers_list(logger,users_ive_followed_from_database):
    #method starts on follower list page and ends on the profile of a random guy
    #randomly scroll
    randomly_scroll_down(logger)

    #click account
    logger.log("Clicking chosen random account.")
    x_coord=187
    y_coord=random.randint(190,1142)
    coord=[x_coord,y_coord]
    click(coord[0],coord[1])
    check_quit_key_press()
    
    #check if account has been targetted
    #get name of current guy
    logger.log("Checking if this account has been targetted before.")
    name=get_name_of_current_profile()
    
    #check if name in file
    if users_ive_followed_from_database.check_if_user_in_users_followed_database(name):
        logger.log("This account has been targetted before. Redoing search algorithm.")
        #if name is found, we need a new name
        #return to list of followers
        get_to_profile_page(logger)
        time.sleep(2)
        check_quit_key_press()
        get_to_followers_page(logger)
        time.sleep(2)
        check_quit_key_press()
        
        #call this method again
        find_random_account_from_followers_list(logger,users_ive_followed_from_database)
    else:
        #if the name isnt in the file, add this name to the file, then return.
        logger.log("Verified that the chosen account is unique. Writing this username to the database.")
        users_ive_followed_from_database.add_username_to_database(name)
        
    
def check_if_name_is_in_file(name,file):
    Lines=file.readlines()
    for line in Lines:
        if line.startswith(name):
            return True
    return False
        

def get_name_of_current_profile():
    #click coord and copy name
    pyautogui.moveTo(205,450,duration=1)
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
    logger.log("Getting a list of the coords of the black follow buttons that appear on the webpage.")
    check_quit_key_press()
    iar=numpy.asarray(screenshot())
    coords_list=[]
    color_black=[15,20,25]
    x_coord=650
    y_coord=190
    while y_coord<1050:
        current_pix=iar[y_coord][x_coord]
        current_coord=[x_coord,y_coord]
        if pixel_is_equal(current_pix,color_black,tol=10):
            coords_list.append(current_coord)
        y_coord+=1
    
    return combine_duplicate_coords(coords_list)


def click_list_of_follow_buttons(follow_button_list,logger):
    length=len(follow_button_list)
    logger.log(f"Clicking the follow buttons that were given. I have {length} coords")
    index=0
    while index<length:
        check_quit_key_press()
        current_coord=follow_button_list[index]
        if (random . randint(1, 3) != 1)or(len(follow_button_list)<5):
            click(current_coord[0],current_coord[1])
            logger.add_follow()
        time.sleep(0.2)
        
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



def handle_restore_pages_notification(logger):
    if check_for_restore_pages_notification():
        click(1117,115)
        logger.log("Handled edge's restore pages notification")
        time.sleep(0.33)


def find_follow_buttons():
    #clear webpage search fucntion; highlighting might get in the way.
    use_webpage_search("t")
    pyautogui.press('backspace')
    
    #get black coords list
    region=[643,400,79,700]
    color_black=[15,20,25]
    color_yellow=[255,255,0]
    
    coords_list_black=find_all_pixels(color=color_black,region=region)
    use_webpage_search('Follow')
    time.sleep(0.33)
    coords_list_yellow=find_all_pixels(color=color_yellow,region=region)
    
    combined_coords_list_black=combine_duplicate_coords(coords_list_black,tol=100)
    combined_coords_list_yellow=combine_duplicate_coords(coords_list_yellow,tol=100)
    
    
    
    return_coord_list=[]
    for black_coord in combined_coords_list_black:
    #for each black coord
        for yellow_coord in combined_coords_list_yellow:
        #loop through every yellow coord seeing if it has similar yellow coords.
            if coords_is_equal(black_coord,yellow_coord,tol=50):
                return_coord_list.append(black_coord)
    
    
    
    return return_coord_list
    
    
    
    