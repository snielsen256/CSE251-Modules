"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Stephen Nielsen
Purpose: Process Task Files

Instructions:  See I-Learn

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.

prime - med-high load - 2 processes  :  Must do calculations with big numbers, but ther eare no loops in the code.
word -- high load ----- 3 processes  :  Nested for-loops make this program a higher load.
upper - Very low load - 1 process    :  Simply adds to the ASCII values of each char.
sum --- high load ----- 2 processes  :  Has a large number of iterations per loop.
name -- medium load --- 2 processes  :  Makes a call to the server for each task.

4 - all requirements met

"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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
 
# task functions

def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    global result_primes

    if is_prime(value):
        return(f"{value} is prime")
    else:
        return(f"{value} is not prime")

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    url = "words.txt"
    word_found = False
    global result_words

    # look for word
    with open(url) as file:
        for line in file:
            for file_word in line:
                if file_word == word:
                    word_found = True
    
    # finish
    if word_found:
        return(f"{word} found")
    else:
        return(f"{word} not found")

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    global result_upper

    upper = str.upper(text)

    return(f"{upper} ==>  uppercase version of {text}")

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    global result_sums
    total = 0

    # find sum
    for i in range(start_value, end_value + 1):
        total += i
    
    # return
    return(f"sum of {start_value:,} to {end_value:,} = {total:,}")

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    global result_names

    response = requests.get(url)

    if response.status_code == 200:
        return(f"{url} has name {response}")
    else:
        return(f"{url} had an error receiving the information")

# callback functions

def cb_prime(response):
    global result_primes
    result_primes.append(response)

def cb_word(response):
    global result_words
    result_words.append(response)

def cb_upper(response):
    global result_upper
    result_upper.append(response)

def cb_sum(response):
    global result_sums
    result_sums.append(response)

def cb_name(response):
    global result_names
    result_names.append(response)


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # constants
    PRIME_PROCESS_COUNT = 2
    WORD_PROCESS_COUNT = 3
    UPPER_PROCESS_COUNT = 1
    SUM_PROCESS_COUNT = 2
    NAME_PROCESS_COUNT = 2


    # TODO Create process pools
    prime_pool = mp.Pool(PRIME_PROCESS_COUNT)
    word_pool = mp.Pool(WORD_PROCESS_COUNT)
    upper_pool = mp.Pool(UPPER_PROCESS_COUNT)
    sum_pool = mp.Pool(SUM_PROCESS_COUNT)
    name_pool = mp.Pool(NAME_PROCESS_COUNT)

    # TODO you can change the following
    # TODO start and wait pools
    

    # determine task type
    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            prime_pool.apply_async(task_prime, args=(task['value'],), callback=cb_prime)
        elif task_type == TYPE_WORD:
            word_pool.apply_async(task_word, args=(task['word'],), callback=cb_word)
        elif task_type == TYPE_UPPER:
            upper_pool.apply_async(task_upper, args=(task['text'],), callback=cb_upper)
        elif task_type == TYPE_SUM:
            sum_pool.apply_async(task_sum, args=(task['start'], task['end']), callback=cb_sum)
        elif task_type == TYPE_NAME:
            name_pool.apply_async(task_name, args=(task['url'],), callback=cb_name)
        else:
            log.write(f'Error: unknown task type {task_type}')
    
    # close and join pools
    prime_pool.close()
    word_pool.close()
    upper_pool.close()
    sum_pool.close()
    name_pool.close()

    prime_pool.join()
    word_pool.join()
    upper_pool.join()
    sum_pool.join()
    name_pool.join()


    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
