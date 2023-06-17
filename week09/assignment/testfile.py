from threading import Thread

def first_function(first_argu, return_val):
    print (first_argu)
    return_val[0]="Return Value from " + first_argu

return_val_from_1=[5]

thread_1 = Thread(target=first_function, args=("Thread 1", return_val_from_1))
print (return_val_from_1)
thread_1.start()

thread_1.join()

print (return_val_from_1)
