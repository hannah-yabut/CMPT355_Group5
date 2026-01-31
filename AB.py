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
    line1 = sys.stdin.readline() # changed to stdin for redirected input as shown in lab 
    line2 = sys.stdin.readline()

    if not line1 or not line2:
        raise ValueError("Expected two lines of input for large and small disk states.")

    large = list(map(int, line1.split())) # list for large disk configuration 
    small = list(map(int, line2.split())) # list for small disk configuration 

    if len(large) != n or len(small) != n: # error checking 
        raise ValueError(f"Expected {n} integers per line.")

    if 0 not in small:
        raise ValueError("Small disks must contain a 0.")

    return State(large, small) # saved as a tuple as in the class State 
  
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
Counts value changes in the circular small disk configuration,
starting after the blank (zero). Not adding after the final copy of a given number is observed.

paramaters:
- state : State object from moves.py

return:
- heuristic value (int)
'''
def h(state):
    obs = state.small
    T = len(obs)

    n = max(obs)                 # number of disks per value
    blank_pos = obs.index(0)     # anchor at the blank

    prev_val = obs[(blank_pos + 1) % T] 

    seen = {v: 0 for v in range(n + 1)} # keeps track of how many of each number is seen
    seen[prev_val] += 1

    h_val = 0

    for step in range(2, T + 1):
        cur_val = obs[(blank_pos + step) % T]
        # If theres a new number, and we know there should still be more of the previous number, increase h_val
        if cur_val != prev_val:
            if prev_val != 0 and seen[prev_val] < n:
                h_val += 1

        seen[cur_val] += 1
        prev_val = cur_val

    return h_val


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
    print(state) # uses __str__
    print("\nFull debug view:")
    print(state.debug_str())

if __name__ == "__main__":
    main()



