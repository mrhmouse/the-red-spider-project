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
def inpt(prompt):
    try: # Just another sign that python 3 sucks.  Deal.
        c = raw_input(prompt)
    except:
        c = input(prompt)
    return c

# https://github.com/blog/699-making-github-more-open-git-backed-wikis
if os.path.exists(os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors"):
    print("You already have a copy of the raptor game data files.  Do you want to update it? (y/n)")
    c = inpt("? ")
    if c == "y":
        print("Downloading raptor game data, please wait...")
        shutil.rmtree(os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors/")
        subprocess.call(["git", "clone", "https://github.com/WesleyAC/the-red-spider-project.wiki.git", os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors"])
        print("Downloaded raptor game data!")
    else:
        print("Ok, keeping the game as is...")
else:
    print("You do not have a copy of the raptor game data files.  Do you want to download them? (y/n)")
    c = inpt("? ")
    if c == "y":
        print("Downloading raptor game data, please wait...")
        subprocess.call(["git", "clone", "https://github.com/WesleyAC/the-red-spider-project.wiki.git", os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors"])
        print("Downloaded raptor game data!")
    else:
        print("You cannot play the raptor game without downloading the data.  Exiting...")
        exit()

croom = "Raptor-Game"
basedir = os.path.expandvars("$RED_SPIDER_ROOT") + "/config/raptors/"
playing = True

def printdata(room):
    lines = room.split("\n")
    chunks = room.split("~~")
    print(lines[0])
    print("")
    print(chunks[1])

def printops(room):
    chunks = room.split("~~")
    ops = chunks[2].split("\n")
    print("Do you want to:")
    i = 0
    for op in ops[1:-1]:
        print(chr(97+i) + ") " + op.split("::")[0])
        i = i + 1

while playing: # main loop
    croomdata = open(basedir + croom + ".md")
    croomtext = croomdata.read()
    printdata(croomtext)
    printops(croomtext)
    c = inpt("")
