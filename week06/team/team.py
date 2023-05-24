"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

def sender(pipe_in, url, word_counter):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(url) as file:
        for line in file:
            for word in line:
                # send words and a space
                pipe_in.send(word)
                word_counter.value += 1
                # send a return after each line
                #pipe_in.send("\n")
                print("sent")


def receiver(pipe_out, url, word_counter):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    words_recieved = 0
    with open(url, 'w') as file:
        while words_recieved < word_counter.value:
            word = pipe_out.recv()
            file.write(word)
            print(word)
            words_recieved += 1
            


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    pipe_in, pipe_out = mp.Pipe()
    
    # TODO create variable to count items sent over the pipe
    word_counter = mp.Value('i', 0)

    # TODO create processes 
    process_sender = mp.Process(target=sender, args=(pipe_in, filename1, word_counter))
    process_reciever = mp.Process(target=receiver, args=(pipe_out, filename2, word_counter))


    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    process_sender.start()
    process_reciever.start()
    print("started")

    # TODO wait for processes to finish
    process_sender.join()
    process_reciever.join()
    print("joined")

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {(stop_time - start_time)}: ')
    log.write(f'items / second = {word_counter.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')

