"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: Stephen Nielsen

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

4 - All requirements met.

"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
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

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


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


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_lot, sem_queue_access, sem_empty_remaining):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs.
        # to create cars and to place them in a queue.
        threading.Thread.__init__(self)
        self.car_lot = car_lot
        self.sem_queue_access = sem_queue_access
        self.sem_empty_remaining = sem_empty_remaining


    def run(self):
        for i in range(CARS_TO_PRODUCE):
            # TODO Add you code here
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
            """
            # acquire
            self.sem_queue_access.acquire()
            # create car and put it in the car_lot
            self.car_lot.put(Car())
            # release
            self.sem_empty_remaining.release()
            



        # signal the dealer that there there are not more cars
        self.car_lot.put("FACTORY FINISHED")
        # release
        self.sem_empty_remaining.release()


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_lot, sem_queue_access, queue_stats, sem_empty_remaining):
        # TODO, you need to add arguments that pass all of data that 1 Dealer needs
        # to sell a car
        threading.Thread.__init__(self)
        self.car_lot = car_lot
        self.sem_queue_access = sem_queue_access
        self.queue_stats = queue_stats
        self.sem_empty_remaining = sem_empty_remaining
        self.count = 0
        

    def run(self):
        while True:
            # TODO Add your code here
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            # acquire
            self.sem_empty_remaining.acquire()

            # get car from car_lot, exit if finished
            if self.car_lot.get() == "FACTORY FINISHED":
                print("THERE ARE NO MORE CARS TO BE SOLD")
                break
            
            # graph
            self.queue_stats[self.car_lot.size()] += 1
            # release
            self.sem_queue_access.release()

            # keep track of how many cars have been sold so far
            self.count += 1
            print(f"CAR NUMBER {self.count} HAS BEEN SOLD")



            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s)
    sem_queue_access = threading.Semaphore(MAX_QUEUE_SIZE) # if 0, queue is empty
    sem_empty_remaining = threading.Semaphore(MAX_QUEUE_SIZE)# if 0, queue is full
    
    # set semaphores to register the queue as empty
    for _ in range(0, MAX_QUEUE_SIZE):
        sem_empty_remaining.acquire()

    # TODO Create queue251 
    car_lot = Queue251()
    # TODO Create lock(s) ?

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    factory = Factory(car_lot, sem_queue_access, sem_empty_remaining)

    # TODO create your one dealership
    dealer = Dealer(car_lot, sem_queue_access, queue_stats, sem_empty_remaining)

    log.start_timer()

    # TODO Start factory and dealership
    factory.start()
    dealer.start()

    # TODO Wait for factory and dealership to complete
    factory.join()
    print("FACTORY THREAD JOINED")
    dealer.join()
    print("DEALER THREAD JOINED")

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
