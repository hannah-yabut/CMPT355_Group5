#!/usr/bin/env python3
from moves import State, Move, SearchNode, LinkedList, ListNode
import heapq # priority algorithm for A* 
from itertools import count # good for large datasets 
import sys # for reading terminal inputs 
sys.argv



# A* implementation 
'''
description: Receives n from terminal input and error checks 
Usage: ./AB n
paramaters: None 
return: n (number of tiles)
'''
def receive_n():
    if len(sys.argv) != 2: 
        print("Usage: ./AB <n>")
        sys.exit(1)

    try: 
        n = int(sys.argv[1])
    except ValueError: 
        print("Error: n must be an integer.")
        sys.exit(1) 
    
    if n <= 0: 
        print("Error: n must be positive")
        sys.exit(1) # exit as an error 
    
    return n 



'''
description: Receives a standard input from keyboard about the initial state of the large and small disks 
paramaters: 
return: State(large, small) , using the State class from moves.py 
'''
def initial_state_input(n): 
    large = list(map(int, input().split())) # take in the 1st terminal input as a list
    small = list(map(int, input().split())) # take in the 2nd terminal input as a list
    
    if len(large) != n or len(small) != n:
        raise ValueError(f"Expected {n} integers per line.")

    if 0 not in small:
        raise ValueError("Small disks must contain a 0.")

    return State(large, small) # saved as a Tuple based on the class State
 

# visited states 
'''
description: hash table/ heap implementation of visited nodes 
paramaters: 
return: 
'''
def S_closed():
    return 0 

'''
description: for the application of the moves 
paramaters: 
return: 
'''
def apply_move() :
    return 0 

# evaluation function, fuction for finding most optimal path using A* 
'''
description: 
paramaters: 
return: 
'''
def f():
    return 0

# heuristic funtion 
'''
description: 
paramaters: 
return: 
'''
def h():
    return 0 

# cost function 
'''
description: 
paramaters: 
return: 
'''
def g():
    return 0 


'''
description: calls helper functions and prints the resulting solution of the puzzle 
paramaters: 
return: 
'''
def main():
    n = receive_n()
    state = initial_state_input(n)

    print("\nState read from input:")
    print(state)            # uses __str__
    print("\nFull debug view:")
    print(state.debug_str())

if __name__ == "__main__":
    main()



