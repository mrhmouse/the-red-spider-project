#!/usr/bin/env python

import os
import subprocess
import shutil
import json

class Option:
    """An option in a room in the raptor game."""
    def __init__(self, pieces):
        length = len(pieces)
        self.death = False
        self.inv = False
        if length == 4:
            if pieces[0] == "INV":
                self.inv = pieces[1]
                self.label = pieces[3]
                self.room = pieces[2]
        elif length == 2:
            self.label = pieces[0]
            self.room = pieces[1]
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

class RaptorGame:
    def __init__(self, game_dir):
        self.game_dir = game_dir
        self.__git_args = [
            "git",
            "clone",
            "https://github.com/WesleyAC/the-red-spider-project.wiki.git",
            self.game_dir
        ]

        self.welcome()
        self.setup()

    def inpt(self, prompt):
        """Display a prompt to the user and return their response."""
        try: # Just another sign that python 3 sucks.  Deal.
            return raw_input(prompt)
        except:
            return input(prompt)

    def ask(self, message, prompt="? "):
        """
        Display a message to the user, then display
        a prompt and wait for a response.
        
        If the response is 'y', return true.
        Else, return false.
        """
        print(message)
        response = self.inpt(prompt)
        return response == "y"


    def clone(self):
        """Clone game data from GitHub."""
        print("Downloading raptor game data, please wait...")
        subprocess.call(self.__git_args)
        print("Downloaded raptor game data!")

    def welcome(self):
        print("""Welcome to the
        ____      _    ____ _____ ___  ____     ____    _    __  __ _____ 
        |  _ \    / \  |  _ \_   _/ _ \|  _ \   / ___|  / \  |  \/  | ____|
        | |_) |  / _ \ | |_) || || | | | |_) | | |  _  / _ \ | |\/| |  _|  
        |  _ <  / ___ \|  __/ | || |_| |  _ <  | |_| |/ ___ \| |  | | |___ 
        |_| \_\/_/   \_\_|    |_| \___/|_| \_\  \____/_/   \_\_|  |_|_____|

                                                                            """)

    def inventory(self, inv):
        """Print the player's current inventory."""
        if not inv == []:
            print("Right now, you are carrying:")
            for item in inv:
                print(" - " + item)
        else:
            print("You don't have anything in your inventory right now!  Go get some lootz!")

    def quit(self, room_name, inv, alreadyhave_inv):
        """Offer the user options to save and quit, or just quit."""
        save = self.inpt("Do you want to save your game? (Y/n)")
        if save == "n":
            print("OK, exiting *without* saving...")
            exit(0)
        else:
            savefile = open(os.path.join(red_spider_root, "config", "raptors", "raptors.json"), "w")
            savefile.write(json.dumps([room_name, inv, alreadyhave_inv]))   
            exit(0)

    def setup(self):
        """Setup the game data, if needed."""
        # https://github.com/blog/699-making-github-more-open-git-backed-wikis
        if os.path.exists(self.game_dir):
            if self.ask("You already have a copy of the raptor game data files. " +
            "Do you want to update it? (y/N) " +
            "WARNING: This may  result in an unplayable game."):
                shutil.rmtree(self.game_dir)
                self.clone()
            else:
                print("Ok, keeping the game as is...")
        else:
            if self.ask("You do not have a copy of the raptor game data files. " +
            "Do you want to download them? (y/N)"):
                self.clone()
            else:
                print("You cannot play the raptor game without downloading the data. " +
                "Exiting...")
                exit(1)
        if os.path.exists(self.game_dir + "/../raptors.json"):
            loadsave = self.inpt("You have a save file.  Do you want to use it? (Y/n)")
            if loadsave == "n":
                print("Ok, starting from the beginning...")
            else:
                gamedata = json.loads(open(os.path.join(red_spider_root, "config", "raptors", "raptors.json")).read())
                self.play_game(gamedata[0], gamedata[1], gamedata[2])
        self.play_game()
            

    def play_game(self, room="Raptor-Game", inventory=[], alreadyhave_inventory=[]):
        room_name = room
        inv = inventory
        alreadyhave_inv = alreadyhave_inventory
        while True:
            try:
                current_room = Room(os.path.join(self.game_dir, room_name + ".md"))
                # Print the room title.
                print(current_room.title)

                # Print the description.
                print(current_room.description)

                # Check for death and inventory
                for option in current_room.options:
                    if option.death:
                        # The player has died.
                        exit(37)
                    if option.inv:
                        alreadyhave = False
                        for item in alreadyhave_inv: # Stop the player from cheating! :P
                            if item == room_name + "/" + option.inv:
                                alreadyhave = True
                        if not alreadyhave:
                            print("You pick up a " + option.inv)
                            inv.append(option.inv)
                            alreadyhave_inv.append(room_name + "/" + option.inv)
                        else:
                            print("You already got the " + option.inv + " from here.")

                # Wait for input.
                valid_response = False
                while not valid_response:
                    # Print each option.
                    i = 0
                    for option in current_room.options:
                        print("{0}) {1}".format(i, option.label))
                        i += 1

                    try:
                        response = self.inpt("")
                        if response == "i":
                            self.inventory(inv)
                        elif response == "exit":
                            self.quit(room_name, inv, alreadyhave_inv)
                        else:
                            response = int(response)
                    except ValueError:
                        print("Please choose a number.")
                        continue

                    if type(response) == int:
                        if len(current_room.options) <= response:
                            print("Please choose one of the listed numbers.")
                            continue

                        room_name = current_room.options[response].room
                        valid_response = True
            except FileNotFoundError:
                print("The story has not been written this far yet.  Do you want to help?")
                print("Go to `https://github.com/WesleyAC/the-red-spider-project/wiki/" +
                        room_name +
                        "/_edit` to decide what happens next!")
                print("Read `https://github.com/WesleyAC/the-red-spider-project/wiki/How-to-make-a-raptor-room` to see how to make a room!")
                exit(2)

if __name__ == "__main__":
    root = os.path.expandvars("$RED_SPIDER_ROOT")
    if root == "$RED_SPIDER_ROOT":
        print("Couldn't find your root directory. Could you point me to it?")
        while True:
            root = input("? ")
            if not os.path.exists(root):
                print("I'm sorry, that doesn't appear to be a valid directory.")
                print("Please input a valid directory.")
                continue
            else:
                break
    root = os.path.join(root, "config", "raptors", "wiki")
    print("Working with folder: ", root)
    game = RaptorGame(root)
