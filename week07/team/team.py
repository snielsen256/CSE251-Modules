"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 07 Team Activity

Instructions:

1) Make a copy of your assignment 2 program.  Since you are 
   working in a team, you can decide which assignment 2 program 
   that you will use for the team activity.

2) Convert the program to use a process pool and use 
   apply_async() with a callback function to retrieve data 
   from the Star Wars website.  Each request for data must 
   be a apply_async() call.

3) You can continue to use the Request_Thread() class from 
   assignment 02 that makes the call to the server.

"""

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790/'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}
        global call_count
        call_count += 1

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)
    
    def get_response(self):
       return self.response
    
# TODO Add any functions you need here


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    mass_thread_list = []

    # TODO Retrieve Top API urls
    print(flush=True)
    t1 = Request_thread(TOP_API_URL)
    t1.start()
    t1.join()
    #print(t1.response)
    

    # TODO Retireve Details on film 6
    t2 = Request_thread(t1.response['films'] + "6") 
    t2.start()
    t2.join()
    #print(t2.response)   

    # create pool
    pool = mp.Pool(5)
    
    # create a thread for each link reference for film 6
    for key, value in t2.response.items():
        if type(value) == type(['']):
          for link in value:
            mass_thread_list.append(Request_thread(link)) # creates a list of anonymous objects. These are referenced only via index of mass_thread_list

    # start pool
    results = [pool.apply_async(x.start, args=(x,)) for x in mass_thread_list]
    # join
    output = [p.get for p in results]

    """
    #start all
    for i in range(0, len(mass_thread_list)):
      mass_thread_list[i].start()

    #join all
    for i in range(0, len(mass_thread_list)):
      mass_thread_list[i].join()        
"""

    # TODO Display results
    # index in mass_thread_list
    id = 0
    # information to leave out
    #omit_list = ["opening_crawl", "episode_id", "created", "edited", "url"]
    print("--------------------------------------------------------")

    for key, value in t2.response.items():
        
        temp_list = [] # Used for sorting. Either creates or ovverides itself here. Must be empty at start of loop.
        
        #skip certain information. Doesnt work with omit_list for some reason
        if "opening_crawl" in key or "episode_id" in key or "created" in key or "edited" in key or "url" in key:
           continue

        # detects lists
        if type(value) == type(['']):
          print()
          # gives a header to the groups (lists)
          print(f"{key.title()}: {len(value)}")
          # iterates through the list, but only for as many as are in a single category.
          for i in value:
            # add name to temp_list
            temp_list.append(mass_thread_list[id].get_response()['name']) 
            # iterates id to point to the next object in mass_thread_list
            id += 1 
          # sort temp_list
          temp_list.sort() 
          # print temp_list
          for name in temp_list:
             print(f"{name}, ", end="")

          print()
          
        else:
          # for non-list information, such as movie title, director, etc.
          print(f"{key.title()}: {value}") 

    
       
    print()
    print("--------------------------------------------------------")
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()