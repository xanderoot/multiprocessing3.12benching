import time
import multiprocessing
import math


'''

notes:
some threads complete sooner than others
this creates 72 total threads that each check its index before creation to help filter out non primes.

'''


start = time.time()

processesToCreate = 72 # doesnt always create that many processes
cyclesToRunPerThread = 20000000
#q = queue.Queue()

def isPrime(input) :
    """ Warning: takes a long time with very large numbers
    
    Args:
        input (int): any int

    Returns:
        Boolean Value: True if prime False if not prime
    """    
    if input == 2: # If the input is 2, it is prime
        return True

    if input % 2 == 0 or input < 2: # If the input is even or less than 2, it is not prime
        return False

    prime = True # Initialize a variable to store the result

    moduloLimit = int(math.sqrt(input)) # Find the square root of the input as the upper limit for checking divisibility

    for i in range(3,moduloLimit + 1, 2) : # Loop through all the odd numbers from 3 to the square root of the input

        if input % i == 0: # If the input is divisible by any number, it is not prime
            prime = False
            break    

    return prime # Return the result

def process_function(number,maxToRun,n):
    start2 = time.time()
    i = number
    totalGenerated = 0
    
    while i < maxToRun:
        if isPrime(i): 
            totalGenerated += 1
        i += 2 * processesToCreate
    if totalGenerated == 0:
        end = time.time()
        print(f"Thread Index {number} completed in {(end - start2):.2f} seconds.")
    #else: 
        #print(totalGenerated)
    n.put(totalGenerated)




numbersGenerated = 0

if __name__ == '__main__':
    #multiprocessing.set_start_method('spawn')
    jobs = []
    manager = multiprocessing.Manager() 
    n = manager.Queue()
    
    childNumber = 1

    while processesToCreate != 0:
        if childNumber % 2 or childNumber % 5 != 0:
            p = multiprocessing.Process(target=process_function, args=(2 * childNumber + 1,cyclesToRunPerThread,n))
            jobs.append(p)
            p.start()
            processesToCreate -= 1
            #print(f"Process {processesToCreate} created.")
        childNumber += 1
        
    for p in jobs:
        p.join()

    while not n.empty():
        item = n.get()
        #print(item)
        numbersGenerated += item
    
    print(f"\n{numbersGenerated} numbers generated")
    end = time.time()

    print(f"Time elapsed: {(end - start):.5f}\n")