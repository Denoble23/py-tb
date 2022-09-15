import sys
import time

import pyautogui
import pyperclip
import PySimpleGUI as sg

from pytb.client import (click_list_of_follow_buttons, find_follow_buttons,
                         find_following_button, get_to_followers_page,
                         get_to_following_page, get_to_profile_page,
                         get_to_random_account_from_followers_list,
                         orientate_terminal, restart_twitter)
from pytb.configuration import load_user_settings
from pytb.database import Database
from pytb.logger import Logger

logger = Logger()
users_ive_followed_from_database = Database("users_ive_followed_from")
user_settings = load_user_settings()
launcher_path = user_settings["launcher_path"]


def main_gui():
    out_text = \
        """
-Python Twitter bot - Matthew Miglio ~June 2022\n\n
-1. Holding space terminates the program, and holding pause pauses the program.\n\n
-2. Specify the location of your microsoft edge in the config file @ \\AppData\\Roaming\\py-tb\\config.json\n
    Make sure the path is specified in the same format as the default example!\n\n
-3. Select a mode:\n
"""
    sg.theme('Material2')

    layout = [
        [sg.Text(out_text)],
        [sg.Radio('Follow mode', "RADIO1", default=True, key="-Follow_IN-")],
        [sg.Radio('Unfollow mode', "RADIO1", default=False, key="-Unfollow_IN-")],

        # buttons
        [sg.Button('Start'), sg.Button('Help'), sg.Button('Donate')]
        # https://www.paypal.com/donate/?business=YE72ZEB3KWGVY&no_recurring=0&item_name=Support+my+projects%21&currency_code=USD
    ]

    window = sg.Window('py-tb', layout)

    while True:
        event, values = read_window(window)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == "Start":
            if values["-Unfollow_IN-"]:
                window.close()
                unfollow_mode_main()
            if values["-Follow_IN-"]:
                window.close()
                follow_mode_main()

        if event == "Donate":
            show_donate_gui()

        if event == "Help":
            show_help_gui()

    window.close()


def show_donate_gui():
    sg.theme('Material2')
    layout = [
        [sg.Text('Paypal donate link: \n\nhttps://www.paypal.com/donate/?business=YE72ZEB3KWGVY&no_recurring=0&item_name=Support+my+projects%21&currency_code=USD'),
         sg.Text(size=(15, 1), key='-OUTPUT-')],

        [sg.Button('Exit'), sg.Button('Copy link to clipboard')]
        # https://www.paypal.com/donate/?business=YE72ZEB3KWGVY&no_recurring=0&item_name=Support+my+projects%21&currency_code=USD
    ]
    window = sg.Window('PY-TwitterBot', layout)
    while True:
        event, values = read_window(window)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == "Copy link to clipboard":
            pyperclip.copy(
                'https://www.paypal.com/donate/?business=YE72ZEB3KWGVY&no_recurring=0&item_name=Support+my+projects%21&currency_code=USD')

    window.close()


def show_help_gui():
    # help menu text
    out_text = ""
    out_text = out_text+"Follow mode information:"
    out_text = out_text+"     -The bot finds people by looking at the followers of your followers. This has a high return rate on follow backs."
    out_text = out_text+"Unfollow mode information:"
    out_text = out_text + \
        "     -The bot unfollows every person that you follow (without discretion)"

    sg.theme('Material2')
    layout = [[sg.Text(out_text)], ]
    window = sg.Window('PY-TwitterBot', layout)
    while True:
        event, values = read_window(window)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    window.close()


def follow_mode_main():
    time.sleep(3)
    orientate_terminal()
    state_restart()
    state_loops = 0
    while True:
        state = "follow_mode"
        if state == "follow_mode":
            state = state_follow_mode()
        if state == "restart":
            state_restart()
            state = "follow_mode"
        if state == "throttled":
            state_throttled()
            state = "follow_mode"

        state_loops = state_loops+1
        print(f"Total state loops?: {state_loops}")


def unfollow_mode_main():
    time.sleep(3)
    orientate_terminal()
    state_restart()
    while True:
        state = "unfollow_mode"
        if state == "unfollow_mode" and state_unfollow_mode() == "restart":
            state = "restart"
        if state == "restart":
            state_restart()
            state = "unfollow_mode"


def state_throttled():
    logger.log("Bot is unable to follow more right now. Waiting 30 minutes.")
    loops=1800
    while loops>0:
        loops=loops-1
        time.sleep(1)
        if (loops % 4 == 0): logger.log(f"Throttled. Waiting {loops} sec more.")


def state_restart():
    logger.add_restart()
    logger.log("-----STATE=restart")
    restart_twitter(logger, launcher_path)


def state_unfollow_mode():
    logger.log("-----STATE=unfollow_mode")

    # get to profile page
    if get_to_profile_page(logger) == "restart":
        return "restart"
    time.sleep(0.33)

    # get to following page
    if get_to_following_page(logger) == "restart":
        return "restart"
    time.sleep(1)

    has_more_to_unfollow = True
    while has_more_to_unfollow:
        has_coords = True
        while has_coords:
            following_button_coord = find_following_button()
            if following_button_coord is None:
                has_coords = False
            else:
                # click 'following' button
                pyautogui.click(
                    x=following_button_coord[0], y=following_button_coord[1], duration=0.33)
                time.sleep(0.33)

                # click 'unfollow' button
                pyautogui.click(597, 667, duration=0.33)

                # add to logger
                logger.add_unfollow()

                logger.log("Unfollowed.")

        # when u run out of coords on screen
        pyautogui.press("f5")
        time.sleep(3)

        # if screen has no followwing buttons then we're done unfollowing
        if find_following_button() is None:
            has_more_to_unfollow = False


def state_follow_mode():
    logger.log("-----STATE=follow_mode")
    while True:
        # get a account to spam follow
        if get_to_random_account_from_followers_list(
            logger, users_ive_followed_from_database)=="restart": return "restart"
        time.sleep(0.33)

        # get to their followers page
        if get_to_followers_page(logger) != "coord_not_found":
            # click that set of coords
            follow_button_list = find_follow_buttons()
            if click_list_of_follow_buttons(follow_button_list, logger) == "throttled":
                return "throttled"
            time.sleep(0.33)

        else:
            logger.log(
                "Had trouble locating the followers button on this profile. Skipping this profile.")


def read_window(window: sg.Window):
    read_result = window.read()
    if read_result is None:
        print("Window not found")
        end_loop()
    return read_result


def end_loop():
    print("Press ctrl-c to close the program.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    try:
        main_gui()
    except Exception as e:
        print(e)
        end_loop()
