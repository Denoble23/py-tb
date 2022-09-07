import json
from os import makedirs
from os.path import exists, expandvars, isdir, join


# r"C:\Users\Matt\Desktop\1\my Programs\twitter bot\config\users_ive_followed_from.txt"

class Database: 
    
    def __init__(self,name):
        self.top_level = join(expandvars(f'%appdata%'), "py-tb")
        self.database_file = join(self.top_level, name)
        self.create_database()


    def check_if_user_in_users_followed_database(self,name):
        with open(self.database_file, 'r') as f:
            lines=f.readlines()
            for current_line in lines :
                if current_line.startswith(name):
                    return True
            return False
               
                
    def create_database(self):
        if not isdir(self.top_level):
            makedirs(self.top_level)
        if not exists(self.database_file):
            with open(self.database_file, "w") as f:
                print("Created database.")
                f.write("test")
        
    def add_username_to_database(self,username_to_add):
        print(f"Added |{username_to_add}| to database file.")
        with open(self.database_file, "a") as f:
            f.write(f"\n{username_to_add}")

