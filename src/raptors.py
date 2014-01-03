#!/usr/bin/env python

import os
import subprocess
import shutil

print("""Welcome to the
 ____      _    ____ _____ ___  ____     ____    _    __  __ _____ 
|  _ \    / \  |  _ \_   _/ _ \|  _ \   / ___|  / \  |  \/  | ____|
| |_) |  / _ \ | |_) || || | | | |_) | | |  _  / _ \ | |\/| |  _|  
|  _ <  / ___ \|  __/ | || |_| |  _ <  | |_| |/ ___ \| |  | | |___ 
|_| \_\/_/   \_\_|    |_| \___/|_| \_\  \____/_/   \_\_|  |_|_____|
                                                                    """)

if os.path.exists(os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors"):
    print("You already have a copy of the raptor game data files.  Do you want to update it? (y/n)")
    try: # Just another sign that python 3 sucks.  Deal.
        c = raw_input("? ")
    except:
        c = input("? ")
    if c == "y":
        print("Downloading raptor game data, please wait...")
        shutil.rmtree(os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors")
        subprocess.call(["git", "clone", "https://github.com/WesleyAC/the-red-spider-project.wiki.git", os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors"])
        print("Downloaded raptor game data!")
    else:
        print("Ok, keeping the game as is...")
else:
    print("You do not have a copy of the raptor game data files.  Do you want to download them? (y/n)")
    try: # Just another sign that python 3 sucks.  Deal.
        c = raw_input("? ")
    except:
        c = input("? ")
    if c == "y":
        print("Downloading raptor game data, please wait...")
        subprocess.call(["git", "clone", "https://github.com/WesleyAC/the-red-spider-project.wiki.git", os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors"])
        print("Downloaded raptor game data!")
    else:
        print("You cannot play the raptor game without downloading the data.  Exiting...")
        exit()
