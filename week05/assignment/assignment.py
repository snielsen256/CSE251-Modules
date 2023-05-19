"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: Stephen Nielsen

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier
- Do not use try...except statements
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

4 - All requirements met

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        #self.display()
    
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')  

class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, sem_queue_access, sem_empty_remaining, barrier, factory_finish_lock):
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        threading.Thread.__init__(self)
        self.car_lot = car_queue
        self.sem_queue_access = sem_queue_access
        self.sem_empty_remaining = sem_empty_remaining
        self.barrier = barrier
        self.lock = factory_finish_lock
        self.finished = False
    
    def get_cars_produced(self):
        return self.cars_to_produce

    def run(self):
        # produce the cars, the send them to the dealerships
        #print(self.cars_to_produce)
        for i in range(0, self.cars_to_produce):
            # acquire
            self.sem_queue_access.acquire()
            # create car and put it in the car_lot
            self.car_lot.put(Car())
            # release
            self.sem_empty_remaining.release()
            #print(i)
        
        # wait until all of the factories are finished producing cars
        #print("pre-barrier")
        self.barrier.wait()
        #print("post-barrier")

        # "Wake up/signal" the dealerships one more time.  Select one factory to do this
        #print("getting lock")
        self.lock.acquire()
        if (not self.finished):
            # signal the dealer that there there are not more cars
            self.car_lot.put("FACTORY FINISHED")
            # release
            self.sem_empty_remaining.release()
            #make sure the other threads know the finihsed signal has been sent
            self.finished = True
        #print("lock released")
        self.lock.release()
            



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_lot, sem_queue_access, sem_empty_remaining):
        #  you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        threading.Thread.__init__(self)
        self.car_lot = car_lot
        self.sem_queue_access = sem_queue_access
        self.sem_empty_remaining = sem_empty_remaining
        self.count = 0
    
    def get_cars_sold(self):
        return self.count


    def run(self):
        while True:
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            # make sure there is an item on the queue
            #print("Getting semaphore")
            self.sem_empty_remaining.acquire()
            #print("Semaphore gotten")

            # get car from car_lot, exit if finished
            if self.car_lot.get() == "FACTORY FINISHED":
                #print("THERE ARE NO MORE CARS TO BE SOLD")
                self.car_lot.put("FACTORY FINISHED")
                self.sem_empty_remaining.release()
                #print("Dealership ending")
                break
            
            # release
            self.sem_queue_access.release()

            # keep track of how many cars have been sold so far
            self.count += 1
            #print(f"CAR NUMBER {self.count} HAS BEEN SOLD")



            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))
            #print(f"sleep after car {self.count}")



def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """
    #print(f"{factory_count} factories, {dealer_count} dealers")

    factory_stats = []

     # Create semaphore(s)
    sem_queue_access = threading.Semaphore(MAX_QUEUE_SIZE) # if 0, queue is empty
    sem_empty_remaining = threading.Semaphore(MAX_QUEUE_SIZE)# if 0, queue is full
    
    # set semaphores to register the queue as empty
    for _ in range(0, MAX_QUEUE_SIZE):
        sem_empty_remaining.acquire()

    # Create queue251 
    car_queue = Queue251()

    # Create barrier and lock
    barrier = threading.Barrier(factory_count)
    factory_finish_lock = threading.Lock()

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)

    # create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    factory_list = [Factory(car_queue, sem_queue_access, sem_empty_remaining, barrier, factory_finish_lock) for _ in range(0, factory_count)]

    # create your dealerships
    dealer_list = [Dealer(car_queue, sem_queue_access, sem_empty_remaining) for _ in range(0, dealer_count)]

    log.start_timer()
    

    # Start all dealerships
    for dealer in dealer_list:
        dealer.start()
    #print("dealers started")
    # Start all factories
    for factory in factory_list:
        factory.start()
    #print("factories started")
    
    # Wait for factories and dealerships to complete
    for factory in factory_list:
        factory.join()
    #print("factories joined")
    for dealer in dealer_list:
        dealer.join()
    #print("dealers joined")
    
    #print("test1")

    # get the number of cars produced by the factories
    for factory in factory_list:
        factory_stats.append(factory.get_cars_produced())   

    # get the number of cars sold by the dealers
    for dealer_index in range(0, len(dealer_list)):
        dealer_stats[dealer_index] = dealer_list[dealer_index].get_cars_sold() 

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factor Stats   : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


