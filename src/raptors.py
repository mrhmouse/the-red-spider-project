#!/usr/bin/env python

import os
import subprocess
import shutil

class Option:
    """An option in a room in the raptor game."""
    def __init__(self, pieces):
        length = len(pieces)
        if length == 2:
            self.label = pieces[0]
            self.room = pieces[1]
            self.death = False
        elif length == 1:
            if pieces[0] == "DIE":
                self.death = True
            else:
                raise Exception("Expected a label and room, but got {0}".format(pieces[0]))
        else:
            raise Exception("Expected a label and a room, but got {0}".format(pieces))

class Room:
    """A room in the raptor game."""

    def fail(message, f):
        raise Exception("While parsing {0}, got exception: {1}".format(f, message))

    def __init__(self, filename):
        """Create a new room, loading the given file."""
        with open(filename) as f:
            self.__parse(iter(f))

    def __parse(self, f):
        """Parse a file, filling out properties of this room."""
        # A room file is laid out as follows:
        #   Title
        #   ~~
        #   Description
        #   ~~
        #   Options
        #   ~~
        #   Comments
        self.__parseTitle(f)

    def __parseTitle(self, f):
        """Parse the title from a room and continue."""
        self.title = ""
        for line in f:
            if line.startswith("~~"):
                break
            self.title += line
        if len(self.title) == 0:
            fail("Expected a title, but couldn't find one.", f)
        self.__parseDescription(f)

    def __parseDescription(self, f):
        self.description = ""
        for line in f:
            if line.startswith("~~"):
                break
            self.description += line
        if len(self.description) == 0:
            fail("Expected a description, but couldn't find one.", f)
        self.__parseOptions(f)

    def __parseOptions(self, f):
        self.options = []
        for line in f:
            if line.startswith("~~"):
                break

            # Skip blank lines
            line = line.strip()
            if len(line) == 0:
                break

            pieces = line.split("::")
            self.options.append(Option(pieces))

        if len(self.options) == 0:
            fail("Expected options, but couldn't find any", f)
        self.__parseComments(f)

    def __parseComments(self, f):
        self.comments = ""
        for line in f:
            self.comments += line

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

### MAIN GAME ###

print("""Welcome to the
 ____      _    ____ _____ ___  ____     ____    _    __  __ _____ 
|  _ \    / \  |  _ \_   _/ _ \|  _ \   / ___|  / \  |  \/  | ____|
| |_) |  / _ \ | |_) || || | | | |_) | | |  _  / _ \ | |\/| |  _|  
|  _ <  / ___ \|  __/ | || |_| |  _ <  | |_| |/ ___ \| |  | | |___ 
|_| \_\/_/   \_\_|    |_| \___/|_| \_\  \____/_/   \_\_|  |_|_____|

                                                                    """)

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
        current_room = Room(os.path.join(GAME_DIR, CROOM + ".md"))
        # Print the room title.
        print(current_room.title)

        # Print the description.
        print(current_room.description)

        # Check for death
        for option in current_room.options:
            if option.death:
                # The player has died.
                exit()

        # Wait for input.
        valid_response = False
        while not valid_response:
            # Print each option.
            i = 0
            for option in current_room.options:
                print("{0}) {1}".format(i, option.label))
                i += 1

            try:
                response = int(inpt(""))
            except ValueError:
                print("Please choose a number.")
                continue

            if len(current_room.options) <= response:
                print("Please choose one of the listed numbers.")
                continue

            CROOM = current_room.options[response].room
            valid_response = True
    except FileNotFoundError:
        print("The story has not been written this far yet.  Do you want to help?")
        print("Go to `https://github.com/WesleyAC/the-red-spider-project/wiki/" + CROOM + "/_edit` to decide what happens next!")
        print("Read `https://github.com/WesleyAC/the-red-spider-project/wiki/How-to-make-a-raptor-room` to see how to make a room!")
        exit()
