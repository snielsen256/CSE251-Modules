"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

Question: is the Python Queue thread safe?  (https://en.wikipedia.org/wiki/Thread_safety)

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 1        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

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
    
def retrieve_thread(q, log):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        item = q.get()
        if item == NO_MORE_VALUES:
            q.put(NO_MORE_VALUES)
            break

        # TODO process the value retrieved from the queue
        # TODO make Internet call to get characters name and log it
        result = Request_thread(item)
        print(result)
        log.write(result)



def file_reader(url, q, log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open(url) as file:
        for line in file:
            q.put(line)

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    q.put(NO_MORE_VALUES)



def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()
    # TODO create semaphore (if needed)

    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job

    t_file_reader = threading.Thread(target=file_reader, args=("urls.txt", q, log))

    queue_pullers_list =[]
    for i in range(0, RETRIEVE_THREADS):
        queue_pullers_list.append[threading.Thread(target=retrieve_thread, args=(q, log))]

    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    t_file_reader.start()
    for reader in queue_pullers_list:
        reader.start()

    # TODO Wait for them to finish - The order doesn't matter
    t_file_reader.join()
    for reader in queue_pullers_list:
        reader.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




