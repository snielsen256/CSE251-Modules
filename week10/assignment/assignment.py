"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Stephen Nielsen

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

This key is repeated several times in the code:
  variables stored in buffer:
      buffer[-1]: read_count - keeps track of how many have been read
      -2:         A countdown of items to write
      -3:         write_index
      -4:         read_index
      -5:         The total number of items to be written


4- All requiremetns met


"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

def write(buffer, writer_can_write, reader_can_read, lock):
    """
    writes to the buffer
    """
    """
    variables stored in buffer:
    buffer[-1]: read_count - keeps track of how many have been read
    -2:         A countdown of items to write
    -3:         write_index
    -4:         read_index
    -5:         The total number of items to be written
    """
    
    while buffer[-2] > 0: # while item_count > 0
        # comfirm writing is possible
        writer_can_write.acquire()

        # write
        with lock:
            buffer[buffer[-3]] = random.randint(1000, 10000)

            # decrement item_count
            buffer[-2] -= 1

            # move write_index forward
            buffer[-3] += 1

            # loop write_index around if at last point
            if buffer[-3] == len(buffer) - (1 + 5): # 1 becasue the list starts at 0, 5 because there are 5 variables in the buffer 
                buffer[-3] = 0

        # indicate that reading is possible
        reader_can_read.release()

def read(buffer, writer_can_write, reader_can_read, lock):
    """
    reads from the buffer
    """
    """
    variables stored in buffer:
    buffer[-1]: read_count - keeps track of how many have been read
    -2:         A countdown of items to write
    -3:         write_index
    -4:         read_index
    -5:         The total number of items to be written
    """
    
    while buffer[-1] < buffer[-5]:
        # confirm reading is possible
        reader_can_read.acquire()

        # read
        with lock:       
            if buffer[-1] >= buffer[-5]:
                break         

            #print(f"{buffer[-1]} of {buffer[-5]}: {buffer[buffer[-4]]}")
            print(buffer[buffer[-4]])

            # record as read
            buffer[-1] += 1

            # move read_index forward
            buffer[-4] += 1

            # loop write_index around if at last point
            if buffer[-4] == len(buffer) - (1 + 5): # 1 becasue the list starts at 0, 5 because there are 5 variables in the buffer
                buffer[-4] = 0

            # indicate that overwriting is ok
            writer_can_write.release()
    

def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))
    
    """
    variables stored in buffer:
    buffer[-1]: read_count - keeps track of how many have been read
    -2:         A countdown of items to write
    -3:         write_index
    -4:         read_index
    -5:         The total number of items to be written
    """
    buffer = smm.ShareableList([0]*(BUFFER_SIZE + 4))
    buffer[-2] = items_to_send
    buffer[-5] = items_to_send

    # Create any lock(s) or semaphore(s) that you feel you need
    """
    Whenever write_index moves forward, reader_can_read is incremented and writer_can_write is decremented.
    Whenever read_index moves forward, reader_can read in decremented and writer_can_write is incremented.
    This ensures that the reader never surpasses the writer, and the writer never overwrites values that haven't been read.
    Semaphores should be checked before the index is moved.
    """
    lock = mp.Lock()
    reader_can_read = mp.Semaphore(0)
    writer_can_write = mp.Semaphore(BUFFER_SIZE)

    # create reader and writer processes
    process_list = []
    
    for _ in range(WRITERS):
        process_list.append(mp.Process(target=write, args=(buffer, writer_can_write, reader_can_read, lock)))

    for _ in range(READERS):
        process_list.append(mp.Process(target=read, args=(buffer, writer_can_write, reader_can_read, lock)))

    # Start the processes and wait for them to finish
    for process in process_list:
        process.start()

    for process in process_list:
        process.join()
    

    print(f'{items_to_send} values sent')

    # Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')

    print(f'{buffer[-1]} values received')

    smm.shutdown()


if __name__ == '__main__':
    main()
