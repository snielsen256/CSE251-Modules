"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

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

# TODO Add any functions you need here


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    mass_thread_list = []

    # TODO Retrieve Top API urls
    print(flush=True)
    #json_reader(TOP_API_URL)
    t1 = Request_thread(TOP_API_URL)
    t1.start()
    t1.join()
    #print(t1.response)
    

    # TODO Retireve Details on film 6
    t2 = Request_thread(t1.response['films'] + "6") 
    t2.start()
    t2.join()
    #print(t2.response)   
    
    # create a thread for each link reference for film 6
    for key, value in t2.response.items():
        if type(value) == type(['']):
          for link in value:
            mass_thread_list.append(Request_thread(link)) 

    #start all
    for i in range(0, len(mass_thread_list)):
      mass_thread_list[i].start()

    #join all
    for i in range(0, len(mass_thread_list)):
      mass_thread_list[i].join()        


    # TODO Display results
    """
    for key, value in range(0, len(t2.response.items())):
        print("" + key + ":")
        print(value)
""" 
      
       

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
