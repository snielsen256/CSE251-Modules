"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)
    
# TODO create read_thread function
def read_thread(url, q, sem_queue_empty):
    with open(url) as file:
        for line in file:
            q.put(line)
            sem_queue_empty.release()
        q.put("FINAL ENTRY")


# TODO create prime_process function
def prime_process(q, list_of_primes, sem_queue_empty):
    while True:
        sem_queue_empty.acquire()
        entry = q.get()

        #check if final entry
        if entry == "FINAL ENTRY":
            q.put(entry)
            break
        else:
            if is_prime(entry):
                list_of_primes.append(entry)


    

def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    q = Queue251()
    sem_queue_empty = threading.Semaphore(0)
    url = 'data.txt'
    process_list = []
    primes = []

    # TODO create reading thread
    reader = threading.Thread(target=read_thread, args=(url, q, sem_queue_empty))

    # TODO create prime processes
    for _ in range(0, PRIME_PROCESS_COUNT):
        process_list.append(mp.Process(target=prime_process, args=(q, primes, sem_queue_empty)))

    # TODO Start them all
    reader.start()
    for i in range(0, PRIME_PROCESS_COUNT):
        process_list[i].start()

    # TODO wait for them to complete
    reader.join()
    for i in range(0, PRIME_PROCESS_COUNT):
        process_list[i].join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

