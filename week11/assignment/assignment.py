"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py

4 - All requirements met
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(index, counter, start_time, party_lock, cleaning_lock):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while (time.time() - start_time) <= TIME:
        # wait
        cleaner_waiting()

        # check if party is active
        room_is_available = party_lock.acquire(False)
        if room_is_available:
            party_lock.release()
        else:
            continue

        # check if there is already a cleaner in the room
        room_is_empty = cleaning_lock.acquire(False)
        if room_is_empty:
            # continue on to the rest of the loop
            pass
        else:
            continue
        
        # clean
        print(STARTING_CLEANING_MESSAGE)
        counter.value += 1 # increment counter
        cleaner_cleaning(index)

        # leave
        print(STOPPING_CLEANING_MESSAGE)
        cleaning_lock.release()

def guest(index, counter, start_time, party_lock, cleaning_lock, active_guests):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while (time.time() - start_time) <= TIME:
        # wait
        guest_waiting()

        #check if not being cleaned
        is_not_being_cleaned = cleaning_lock.acquire(False)
        if is_not_being_cleaned:
            cleaning_lock.release()
        else:
            continue

        # check if party is active
        # NOTE -- at this point in the loop, it is assumed that the room is not being cleaned
        is_first_to_party = party_lock.acquire(False)
        if is_first_to_party:
            print(STARTING_PARTY_MESSAGE)
            counter.value += 1 # increment party counter
        
        # increment the number of active guests, regardless if they are the first or not
        active_guests.value += 1

        # party
        guest_partying(index, active_guests.value)

        # leave
        active_guests.value -= 1

        # display message if last
        if active_guests.value <= 0:
            party_lock.release()
            print(STOPPING_PARTY_MESSAGE)
        

def main():
    # Start time of the running of the program. 
    start_time = time.time()

    # add any variables, data structures, processes you need
    cleaner_list = []
    guest_list = []
    party_lock = mp.Lock() # this is the "light switch"
    cleaning_lock = mp.Lock()
    active_guests = mp.Value("i", 0) # the number of guests in the room
    cleaned_count = mp.Value("i", 0)
    party_count = mp.Value("i", 0)


    # add any arguments to cleaner() and guest() that you need
    for index in range(1, CLEANING_STAFF):
        cleaner_list.append(mp.Process(target=cleaner, args=(index, cleaned_count, start_time, party_lock, cleaning_lock)))

    for index in range(1, HOTEL_GUESTS):
        guest_list.append(mp.Process(target=guest, args=(index, party_count, start_time, party_lock, cleaning_lock, active_guests)))

    # start and join processes
    for g in guest_list:
        g.start()
    
    for c in cleaner_list:
        c.start()
    
    for g in guest_list:
        g.join()
    
    for c in cleaner_list:
        c.join()


    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()

