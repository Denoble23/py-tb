import random
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

from image_rec import check_for_location, coords_is_equal, find_references, get_first_location, pixel_is_equal


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


def click(x, y, clicks=1, interval=0.0):
    original_pos = pyautogui.position()
    loops = 0
    while loops < clicks:
        check_quit_key_press()
        pyautogui.click(x=x, y=y)
        pyautogui.moveTo(original_pos[0], original_pos[1])
        loops = loops + 1
        time.sleep(interval)


def check_quit_key_press():
    if keyboard.is_pressed("space"):
        print("Space is held. Quitting the program")
        sys.exit()
    if keyboard.is_pressed("pause"):
        print("Pausing program until pause is held again")
        time.sleep(2)
        pressed=False
        while not(pressed):
            time.sleep(0.05)
            if keyboard.is_pressed("pause"):
                print("Pause held again. Resuming program.")
                pressed=True 


def screenshot(region=(0, 0, 1200, 1200)):
    if region is None:
        return pyautogui.screenshot()
    else:
        return pyautogui.screenshot(region=region)


def orientate_twitter_window(logger):
    logger.log('Looking for window')

    twitter_window = pygetwindow.getWindowsWithTitle(
        "Twitter -")[0]
    time.sleep(1)
    
    
    logger.log('Minimizing')
    twitter_window.minimize()
    logger.log('Restoring')
    twitter_window.restore()
    twitter_window.restore()
    
    time.sleep(1)
    
    logger.log('Moving to topleft')
    twitter_window.moveTo(0, 0)
    time.sleep(1)

    logger.log('Setting size.')
    twitter_window.resizeTo(1200, 1200) # set size to 100x100
    time.sleep(1)


def restart_twitter(logger, launcher_path):
    #if twitter is open, close it.
    windows = pygetwindow.getAllTitles()
    index=len(windows)-1
    logger.log("Checking if twitter already open.")
    while index>-1:
        if str(windows[index]).startswith("Twitter -"):
            logger.log("Twitter is open. Closing it.")
            twitter_window=pygetwindow.getWindowsWithTitle('Twitter -')[0]
            twitter_window.close() 
            time.sleep(2)
        index=index-1

    #open twitter
    logger.log("Opening Twitter.")
    
    os.startfile(launcher_path)
    time.sleep(5)
    
    #orientate twitter
    orientate_twitter_window(logger)
    
    
def get_to_profile_page(logger):
    logger.log("Getting to profile page.")
    check_quit_key_press()
    #click profile icon on the left side
    logger.log('Clicking profile page')
    click(98,472,clicks=3,interval=0.2)
    time.sleep(2)
    
    
def get_to_following_page(logger):
    #check if on profile page
    logger.log("Checking if we're on the profile page.")
    if not(check_if_on_twitter_main()):
        logger.log("We're not somewhere on the profile page.")
        return
    else:
        logger.log("We're somewhere on the profile page.")
    
    #if we're on profile page click following logo
    following_button_location=find_following_button()
    logger.log(f"Location of following button is {following_button_location}")
    if following_button_location is None:
        logger.log("Couldn't find find the following button.")
        return
    logger.log(f"Clicking following button.")
    click(following_button_location[0],following_button_location[1])
    
 
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
    
    iar=numpy.asarray(screenshot())
    x_coord=307
    while x_coord<386:
        y_coord=439
        while y_coord<478:
            #for each pixel
            current_pix=iar[y_coord][x_coord]
            sentinel=[255,150,50]
            if pixel_is_equal(current_pix,sentinel,tol=15):
                return [x_coord,y_coord]
            
            y_coord=y_coord+1
        x_coord=x_coord+1
        
    return None


def look_for_unfollow_button_in_unfollow_page(logger):
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


def find_all_pixels(region,color):
    #searches entire region for pixel and returns a list of the coords of every positive pixel.
    
    #make list of coords
    coords_list = []
    
    #make image-as-array
    iar=numpy.asarray(screenshot())
    
    x_coord=region[0]
    while x_coord<(region[0]+region[2]):
        y_coord=region[1]
        while y_coord<(region[1]+region[3]):
            #for each pixel in region
            iar_pix=iar[y_coord][x_coord]
            current_pix=[iar_pix[0],iar_pix[1],iar_pix[2]]
            current_coord=[x_coord,y_coord]
        
            #add all postiive pixels to return list
            if pixel_is_equal(color,current_pix,tol=15):
                coords_list.append(current_coord)
                
            y_coord=y_coord+1
        x_coord=x_coord+1
        
    return coords_list


def get_to_followers_page(logger):
    logger.log("Getting to this profile's followers page")
    check_quit_key_press()
    use_webpage_search("Followers")
    region=[154,421,311,200]
    
    color=[255,150,50]
    coords_list=find_all_pixels(region,color)
    coord=coords_list[0]
    
    click(coord[0],coord[1],clicks=1)
    

def find_followers_button_on_profile_to_follow_from():
    #search for following
    use_webpage_search('Following')
    
    #search for orange pixel
    region=[252,275,550,70]
    color=[255,150,50]
    return search_region_for_pixel(region,color)
    
   
def combine_duplicate_coords(coords_list):
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
        if not(check_if_coord_in_coord_list(current_coord,new_coords_list)):
            new_coords_list.append(current_coord)
        
        #increment
        index=index+1
        
    return new_coords_list
    
        
def check_if_coord_in_coord_list(coord,coord_list):
    #loop vars
    index=0
    total_coords_in_coords_list=len(coord_list)
    
    while index<total_coords_in_coords_list:

        #get curent coord
        current_coord=coord_list[index]

        
        #compare current coord with coord in question
        if coords_is_equal(current_coord,coord,tol=50):
            return True
        
        #increment
        index=index+1
    
    #if we make it out of the loop without ever returning True then that means the coord is unique
    return False


def find_random_account_from_followers_list(logger):
    #method starts on follower list page and ends on the profile of a random guy
    #randomly scroll
    logger.log("Randomly scrolling.")
    scrolls=random.randint(5,30)
    while scrolls>0:
        logger.log("Scrolling")
        click(1183,1151)
        time.sleep(0.2)
        if random.randint(1,6)==3:
            time.sleep(3)
        scrolls-=1

    #click account
    logger.log("Clicking chosen random account.")
    x_coord=random.randint(187,571)
    y_coord=random.randint(175,1167)
    coord=[x_coord,y_coord]
    click(coord[0],coord[1])
    check_quit_key_press()
    
    #open list of users ive already spammed
    logger.log("Checking if this account has been targetted before.")
    dir=r"C:\Users\Matt\Desktop\1\my Programs\twitter bot\config\users_ive_followed_from.txt"
    file=open(dir)
    
    #get name of current guy
    name=get_name_of_current_profile()
    
    #check if name in file
    if check_if_name_is_in_file(name,file):
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
        find_random_account_from_followers_list(logger)
    else:
        #if the name isnt in the file, add this name to the file, then return.
        logger.log("Verified that the chosen account is unique. Writing this username to the database.")
        dir=r"C:\Users\Matt\Desktop\1\my Programs\twitter bot\config\users_ive_followed_from.txt"
        file=open(dir,'a')
        name=f"\n{name}"
        file.writelines(name)

    
def check_if_name_is_in_file(name,file):
    Lines=file.readlines()
    for line in Lines:
        if line.startswith(name):
            return True
    return False
        

def get_name_of_current_profile():
    #click coord and copy name
    pyautogui.moveTo(183,405,duration=1)
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
    x_coord=694
    y_coord=251
    while y_coord<980:
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
        if not(random.randint(1,3)==1):
            click(current_coord[0],current_coord[1])
            logger.add_follow()
        time.sleep(0.2)
        
        index+=1
        



    
        
    


