import json
from os import makedirs
from os.path import exists, expandvars, isdir, join


# r"C:\Users\Matt\Desktop\1\my Programs\twitter bot\config\users_ive_followed_from.txt"

top_level = join(expandvars(f'%appdata%'), "py-tb")
database_file = join(top_level, 'users_ive_followed_from.txt')


def check_if_user_in_users_followed_database(name):
    with open(database_file, 'r') as f:
        lines=f.readlines()
        for current_line in lines :
            if current_line.startswith(name):
                return True
        return False
            


def create_database():
    if not isdir(top_level):
        makedirs(top_level)
    if not exists(database_file):
        with open(database_file, "w") as f:
            f.write("test")
    
    
create_database()

