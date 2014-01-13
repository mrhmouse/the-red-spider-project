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
    """Display a prompt to the user and return their response."""
    try: # Just another sign that python 3 sucks.  Deal.
        return raw_input(prompt)
    except:
        return input(prompt)

def ask(message, prompt="? "):
    """
    Display a message to the user, then display
    a prompt and wait for a response.
    
    If the response is 'y', return true.
    Else, return false.
    """
    print(message)
    response = inpt(prompt)
    return response == "y"

def clone():
    """Clone game data from GitHub."""
    print("Downloading raptor game data, please wait...")
    subprocess.call(["git", "clone", "https://github.com/WesleyAC/the-red-spider-project.wiki.git", GAME_DIR])
    print("Downloaded raptor game data!")

def printdata(room):
    """TODO: Document this."""
    lines = room.split("\n")
    chunks = room.split("~~")
    print(lines[0])
    print("")
    print(chunks[1])

def printops(room):
    """TODO: Document this."""
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
    """TODO: Document this."""
    global CROOM
    chunks = room.split("~~")
    ops = chunks[2].split("\n")
    i = 0
    for op in ops:
        if not (op.split("::")[0] == ""):
            if inp == chr(97+i):
                CROOM = op.split("::")[1]
            i = i + 1

### MAIN GAME ###

# https://github.com/blog/699-making-github-more-open-git-backed-wikis
# Setup the game data, if needed.
if os.path.exists(GAME_DIR):
    if ask("You already have a copy of the raptor game data files.  Do you want to update it? (y/N)"):
        shutil.rmtree(GAME_DIR)
        clone()
    else:
        print("Ok, keeping the game as is...")
else:
    if ask("You do not have a copy of the raptor game data files.  Do you want to download them? (y/N)"):
        clone()
    else:
        print("You cannot play the raptor game without downloading the data.  Exiting...")
        exit()


while PLAYING: # main loop
    try:
        current_room = open(os.path.join(GAME_DIR, CROOM + ".md")).read()
        printdata(current_room)
        printops(current_room)
        gotoroom(inpt(""), current_room)
    except FileNotFoundError:
        print("The story has not been written this far yet.  Do you want to help?")
        print("Go to `https://github.com/WesleyAC/the-red-spider-project/wiki/" + CROOM + "/_edit` to decide what happens next!")
        print("Read `https://github.com/WesleyAC/the-red-spider-project/wiki/How-to-make-a-raptor-room` to see how to make a room!")
        exit()
