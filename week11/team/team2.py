"""
Course: CSE 251
Lesson Week: 11
File: team2.py
Author: Brother Comeau

Purpose: Team Activity 2: Queue, Stack

Instructions:

Part 1:
- Create classes for Queue_t and Stack_t that are thread safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple threads.

Part 2
- Create classes for Queue_p and Stack_p that are process safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple processes.

Queue methods:
    - constructor(<no arguments>)
    - size()
    - get()
    - put(item)

Stack methods:
    - constructor(<no arguments>)
    - push(item)
    - pop()

Steps:
1) write the Queue_t and test it with threads.
2) write the Queue_p and test it with processes.
3) Implement Stack_t and test it 
4) Implement Stack_p and test it 

Note: Testing means having lots of concurrency/parallelism happening.  Also
some methods for lists are thread safe - some are not.

"""
import time
import threading
import multiprocessing as mp

# -------------------------------------------------------------------
class Queue_t:
    def __init__(self):
        self.arr = []
        self.lock = threading.Lock()

    def size(self):
        self.lock.acquire()
        size = len(self.arr)
        self.lock.release()
        return size

    def put(self, item):
        self.lock.acquire()
        self.arr.append(item)
        self.lock.release()

    def get(self):
        self.lock.acquire()
        item = self.arr.pop(0)
        self.lock.release()
        return item

# -------------------------------------------------------------------
class Stack_t:
    def __init__(self):
        self.arr = []
        self.lock = threading.Lock()

    def push(self, item):
        self.lock.acquire()
        self.arr.append(item)
        self.lock.release()

    def pop(self):
        self.lock.acquire()
        item = self.arr.pop(-1)
        self.lock.release()
        return item

# -------------------------------------------------------------------
class Queue_p:
    def __init__(self):
        self.arr = []
        self.lock = mp.Lock()

    def size(self):
        self.lock.acquire()
        size = len(self.arr)
        self.lock.release()
        return size

    def put(self, item):
        self.lock.acquire()
        self.arr.append(item)
        self.lock.release()

    def get(self):
        self.lock.acquire()
        item = self.arr.pop(0)
        self.lock.release()
        return item

# -------------------------------------------------------------------
class Stack_p:
    def __init__(self):
        self.arr = []
        self.lock = mp.Lock()

    def push(self, item):
        self.lock.acquire()
        self.arr.append(item)
        self.lock.release()

    def pop(self):
        self.lock.acquire()
        item = self.arr.pop(-1)
        self.lock.release()
        return item

def test_q_t(q):
    print("Put 5")
    q.put(5)
    print(f"Size: {q.size()}")
    print(f"Get: {q.get()}")


def main():
    pass
    # test Queue_t
    test_list = []
    q = Queue_t()
    for i in range(3):
        test_list.append(threading.Thread(target=test_q_t, args=(q,)))
    
    for i in test_list:
        i.start()

    for i in test_list:
        i.join()
    
    
    # test Stack_t

    # test Queue_p

    # test Stack_p



if __name__ == '__main__':
    main()
