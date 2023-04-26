"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls
Website is: http://deckofcardsapi.com

Instructions:

- Review instructions in I-Learn.

2p4f4uhto4d3

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    
    

    def __init__(self, request):
        threading.Thread.__init__(self)
        self.parameters = request
        self.response = {}
    
    def run(self):
        response = requests.get(self.parameters)
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)



    




class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        print('Reshuffle Deck')
        # TODO - add call to reshuffle
        #t = Request_thread("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
        t = Request_thread(f"https://deckofcardsapi.com/api/deck/{self.id}/shuffle/")
        t.start()
        t.join()


    def draw_card(self):
        # TODO add call to get a card
        t = Request_thread(f"https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=2")
        t.start()
        t.join()

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = '2p4f4uhto4d3'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

