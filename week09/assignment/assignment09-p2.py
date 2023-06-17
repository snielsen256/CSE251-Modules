"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Stephen Nielsen

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

<Answer here>

Why would it work?

<Answer here>

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

def move_forward(maze, position, lock, color, response_list):
    """
    Returns an empty list if a dead end, or a list of valid moves if there is a split. 
    Calls itelf if there is only one way forward.
    """
    print("------")
    global stop
    row = position[0]
    col = position[1]
    possible_moves = []
    valid_moves = []

    # Critical sections - do the actions that require access to the maze ----------------
    with lock:
        # get possible moves
        print("Analyzing surroundings")
        possible_moves = maze.get_possible_moves(row, col)
    
    with lock:    
        # mark current position as visited
        print("Marking territory")
        maze.move(row, col, color)
         
    with lock: 
        # check if finished
        print("Checking destination")
        if maze.at_end(row, col):
            stop = True
            #return []
            print("The journey is over")
            #responses.append([])
            return
        
    # make a list of valid moves
    print("Confirming valid routes")
    for motion in possible_moves:
        with lock:
            if maze.can_move_here(motion[0], motion[1]):
                valid_moves.append(motion)
    
    # end of critical sections ----------------------------------------------------------
    
    print(f"Response_list from thread's perspective - before change: {response_list}")
    
    # make decision based on length of valid_moves
    if len(valid_moves) == 0:
        # dead end
        print(f"There is no way forward: {valid_moves}")
        return
    elif len(valid_moves) > 1:
        # split
        print(f"The path is uncertain: {valid_moves}")
        for move_index in range(len(valid_moves)):
            response_list[move_index] = valid_moves[move_index]
        print(f"Response_list from thread's perspective - after change: {response_list}")
        return
    else:
        # only one way forward
        print(f"The way is clear: {valid_moves}")
        # critical section --------------------------------------------------------------
        with lock:
            maze.move(valid_moves[0][0], valid_moves[0][1], color)
        # end of critical section -------------------------------------------------------
        move_forward(maze, valid_moves[0], lock, color, response_list)
        return
        
def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global stop
    stop = False
    thread_list = []
    responses = [None]*3
    responses_secondary = [None]*3 # "responses_secondary" allows for an empty "responses" list to be given to the threads called using the data from "responses"

    # create lock
    lock = threading.Lock()

    # make first thread
    thread_list.append(threading.Thread(target=move_forward, args=(maze, maze.get_start_pos(), lock, get_color(), responses)))
    print(thread_list)

    #while not stop:
    for _ in range(0, 3):
        # clear responses list 
        responses = [None]*3
        responses_secondary = [None]*3

        # start all threads in thread_list
        print("Starting threads")
        for i in range(0, len(thread_list)):
            thread_list[i].start()
        
        print("Joining threads")
        # join the threads and get the return lists
        for i in range(0, len(thread_list)):
            thread_list[i].join()

        # clear thread_list
        thread_list = []

        print(f"pre-shift responses:{responses}")
        print(f"pre-shift responses_secondary:{responses_secondary}")
        
        # transfer data from responses to responses_secondary
        for move_index in range(len(responses)):
            responses_secondary[move_index] = responses[move_index]

        # clear responses list, just in case 
        responses = [None]*3

        print(f"post-shift responses:{responses}")
        print(f"post-shift responses_secondary:{responses_secondary}")

        # if the new threads split, make a new thread for each direction
        for direction_set in responses_secondary:
            if direction_set is None:
                continue
            else:
                for motion in direction_set:
                    if motion is None:
                        continue
                    else:
                        thread_list.append(threading.Thread(target=move_forward, args=(maze, motion, lock, get_color(), responses)))

def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True


def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)


if __name__ == "__main__":
    main()