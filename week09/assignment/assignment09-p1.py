"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: Stephen Nielsen

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
SLOW_SPEED = 100
FAST_SPEED = 1
speed = SLOW_SPEED

def move_forward(maze, position, path):
    row = position[0]
    col = position[1]
    possible_moves = maze.get_possible_moves(row, col)

    # mark current position as visited
    maze.restore(row, col)

    # append position to path
    path.append(position)

    # check if finished
    if maze.at_end(row, col):
        #return True
        return path
    # check if dead end
    if len(possible_moves) == 0:
        return False
    
    #print(f"From {row}, {col} you can move to {possible_moves}")
    
    # go down each open path
    for motion in possible_moves:

        # check if movement is valid
        if not maze.can_move_here(motion[0], motion[1]):
            continue

        # if path is not the correct path
        correct_path = move_forward(maze, motion, path)
        if not correct_path:
            continue
        else:
            return path
            
                    

def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
        
    # TODO start add code here
    path = []
    start = maze.get_start_pos()
    path = move_forward(maze, start, path)
    return path


def get_path(log, filename):
    """ Do not change this function """
    #  'Maze: Press "q" to quit, "1" slow drawing, "2" faster drawing, "p" to play again'
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()