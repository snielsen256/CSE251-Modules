"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Stephen Nielsen
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.

4 - all requirements met
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'

class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, wait_time, sender, marble_count):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.sender = sender
        self.wait_time = wait_time
        self.marble_count = marble_count

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for i in range(0, self.marble_count):
            # wait
            time.sleep(self.wait_time)
            # send
            self.sender.send(random.choice(self.colors))
            #print(f"Marble {i+1} of {self.marble_count} created")

        #last item
        self.sender.send("FINISHED")
        print("creator done")
        return 0
            

class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, wait_time, sender, reciever, marbles_per_bag):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.sender = sender
        self.reciever = reciever
        self.wait_time = wait_time
        self.marbles_per_bag = marbles_per_bag

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            # wait
            time.sleep(self.wait_time)
            #print("bagger ready")

            # create empty bag
            bag = Bag()
            #print("bag created")

            # loop per marble
            #print(f"{self.marbles_per_bag} marbles per bag")
            for i in range(0, self.marbles_per_bag):
                marble = self.reciever.recv()
                #print(f"marble {marble} recieved, number {i+1} of {self.marbles_per_bag}")

                #check for end
                if (marble == "FINISHED"):
                    self.sender.send("FINISHED")
                    print("bagger done")
                    return 0
                
                #fill bag
                bag.add(marble)
                #print("marble added to bag")
            
            # send bag
            #print("ready to send bag")
            self.sender.send(bag)
            #print("Bag sent")

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, wait_time, sender, reciever):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.sender = sender
        self.reciever = reciever
        self.wait_time = wait_time

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''

        while True:
            # wait
            #print("assembler ready")
            time.sleep(self.wait_time)

            # get bag
            self.bag = self.reciever.recv()
            #print("bag recieved")

            # check for end
            if (self.bag == "FINISHED"):
                self.sender.send("FINISHED")
                print("assembler done")
                return 0
            
            # assemble and send
            self.sender.send(Gift(random.choice(self.marble_names), self.bag))
            #print("gift sent")

class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, wait_time, reciever, url, gift_count):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.reciever = reciever
        self.url = url
        self.wait_time = wait_time
        self.gift_count = gift_count

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''

        with open(self.url, 'w') as file:
            while True:
                # wait
                time.sleep(self.wait_time)

                # get gift
                self.item = self.reciever.recv()

                #check for end
                if (self.item == "FINISHED"):
                    print("wrapper done")
                    return 0
                
                # write to file
                file.write(f"{datetime.now().time()} {self.item}\n")
                

                # increement gift_count
                self.gift_count.value += 1
                #print(f"item {self.gift_count.value} written to file")
        
                
def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')

def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # create Pipes between creator -> bagger -> assembler -> wrapper
    creator_sender, bagger_reciever = mp.Pipe()
    bagger_sender, assembler_reciever = mp.Pipe()
    assembler_sender, wrapper_reciever = mp.Pipe()

    # create variable to be used to count the number of gifts
    gift_count = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)
    
    log.write('Create the processes')

    # Create the processes (ie., classes above)
    creator = Marble_Creator(settings[CREATOR_DELAY], creator_sender, settings[MARBLE_COUNT])
    bagger = Bagger(settings[BAGGER_DELAY], bagger_sender, bagger_reciever, settings[NUMBER_OF_MARBLES_IN_A_BAG])
    assembler = Assembler(settings[ASSEMBLER_DELAY], assembler_sender, assembler_reciever)
    wrapper = Wrapper(settings[WRAPPER_DELAY], wrapper_reciever, BOXES_FILENAME, gift_count)

    log.write('Starting the processes')
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.
    print(f"{gift_count.value} gifts created")

if __name__ == '__main__':
    main()

