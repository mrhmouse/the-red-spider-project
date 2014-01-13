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

RED_SPIDER_ROOT = os.path.expandvars("$RED_SPIDER_ROOT")
GAME_DIR = os.path.join(RED_SPIDER_ROOT, "config", "raptors")
CROOM = "Raptor-Game"
PLAYING = True


def inpt(prompt):
    try: # Just another sign that python 3 sucks.  Deal.
        return raw_input(prompt)
    except:
        return input(prompt)

# https://github.com/blog/699-making-github-more-open-git-backed-wikis
if os.path.exists(GAME_DIR):
    print("You already have a copy of the raptor game data files.  Do you want to update it? (y/N)")
    c = inpt("? ")
    if c == "y":
        print("Downloading raptor game data, please wait...")
        shutil.rmtree(GAME_DIR)
        subprocess.call(["git", "clone", "https://github.com/WesleyAC/the-red-spider-project.wiki.git", GAME_DIR])
        print("Downloaded raptor game data!")
    else:
        print("Ok, keeping the game as is...")
else:
    print("You do not have a copy of the raptor game data files.  Do you want to download them? (y/N)")
    c = inpt("? ")
    if c == "y":
        print("Downloading raptor game data, please wait...")
        subprocess.call(["git", "clone", "https://github.com/WesleyAC/the-red-spider-project.wiki.git", GAME_DIR)
        print("Downloaded raptor game data!")
    else:
        print("You cannot play the raptor game without downloading the data.  Exiting...")
        exit()

def printdata(room):
    lines = room.split("\n")
    chunks = room.split("~~")
    print(lines[0])
    print("")
    print(chunks[1])

def printops(room):
    chunks = room.split("~~")
    ops = chunks[2].split("\n")
    if ops[1] == "DIE":
        exit()
    print("Do you want to:")
    i = 0
    for op in ops:
        if not (op.split("::")[0] == ""):
            print(chr(97+i) + ") " + op.split("::")[0])
            i = i + 1

def gotoroom(inp, room):
    global CROOM
    chunks = room.split("~~")
    ops = chunks[2].split("\n")
    i = 0
    for op in ops:
        if not (op.split("::")[0] == ""):
            if inp == chr(97+i):
                CROOM = op.split("::")[1]
            i = i + 1

while PLAYING: # main loop
    try:
        current_room = open(os.path.join(GAME_DIR, CROOM + ".md")).read()
        printdata(current_room)
        printops(current_room)
        gotoroom(inpt(""), current_room)
    except FileNotFoundError:
        print("The story has not been written this far yet.  Do you want to help?\nGo to `https://github.com/WesleyAC/the-red-spider-project/wiki/" + CROOM + "/_edit` to decide what happens next!\nRead `https://github.com/WesleyAC/the-red-spider-project/wiki/How-to-make-a-raptor-room` to see how to make a room!")
        exit()
