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

def initial_state_input_test():
    large = [1, 2, 2, 1, 3]
    small = [1, 1, 2, 2, 0]
    return State(large, small)


# visited states 
'''
description: hash table/ heap implementation of visited nodes 
paramaters: 
return: 
'''
def S_closed():
    return 0 

#currently expanding node
'''
Description: implementation for the current node, i dont really know if it fits any of the current so paste it into the appropriate spot (im sorry)
parameters: heap
return: lowest cost node in the frontier(hashtable)
'''
def curr(heap, frontier):
    curr_node = heapq.heappop(heap)[2]
    key = hash(curr_node)
    state = frontier.get(key)
    return state

#frontier
'''
Description: store state (nodes) into frontier based on evaluation function and heuristic
parameters: SearchNode(state), heap, hashtable
return: none
'''
def into_frontier(heap, SearchNode, frontier):
    heapq.heappush(heap, (SearchNode.h, SearchNode.g, SearchNode))
    key = hash(SearchNode)
    frontier.update({key: SearchNode})
    return 0

'''
description: for the application of the moves 
paramaters: state (State):- An instance of the State object
            side (string) :- "R" to move right, "L" to move left
            k (int) :- number of steps to move
return: New instance of the State object with a new state
'''
def apply_move(state, side, k) :
    
    small_state = list(state.small)
    n = len(small_state)
    
    zero_index = small_state.index(0)

    if side == "R":
        destination_index = (zero_index + k) % n
    else:
        destination_index = (zero_index - k) % n

    new_state = small_state

    # swap zero with destination position
    new_state[zero_index], new_state[destination_index] = new_state[destination_index], new_state[zero_index] 

    return State(state.large, tuple(new_state))
    

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
Gap-based heuristic with cyclic ordering awareness.
Counts a gap when:
- leaving a value before all n copies are seen, OR
- the ordering jumps incorrectly in the 1..n cycle once observing the last of a set of numbers (eg. moving from the final 1, we expect a 2 etc.)

The "first" flag stays True through the initial run (starting value).
On the first switch away from that value, we do not count a gap if 0 is
splitting the same value across the ends of the circular list.

paramaters:
- state : State object from moves.py

return:
- heuristic value (int)
'''
def h(state):
    obs = state.small
    T = len(obs)
    n = max(obs)

    zero_pos = obs.index(0)
    before_zero = obs[(blank_pos - 1) % T]

    prev = obs[(blank_pos + 1) % T]   # first value after 0 (nonzero)

    seen = {v: 0 for v in range(n + 1)}
    seen[prev] += 1

    h_val = 0
    first = True  # stays True until we leave the starting run

    # stop before we wrap back onto 0, so cur_val is never 0
    for step in range(2, T):
        cur = obs[(zero_pos + step) % T]

        if cur != prev:
            # first boundary leaving the starting run:
            # ignore if 0 is splitting the same value
            if not (first and before_zero == prev):
                if seen[prev] < n:
                    h_val += 1
                elif cur != ((prev % n) + 1):
                    h_val += 1

            first = False

        seen[cur] += 1
        prev = cur

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
    #n = receive_n()
    #state = initial_state_input(n)
    state = initial_state_input_test()
    state1 = State(state.large, "12120")
    state2 = State(state.large, "12210")

    sn = SearchNode(state, g=3, h=1)
    sn1 = SearchNode(state1, g=2, h=1)
    sn2 = SearchNode(state2, g=4, h=1)


    print("\nState read from input:")
    print(state) # uses __str__
    print("\nFull debug view:")
    print(state.debug_str())
    heap = []
    frontier = {}
    into_frontier(heap, sn, frontier)
    into_frontier(heap, sn1, frontier)
    into_frontier(heap, sn2, frontier)
    print(str(curr(heap,frontier).state))

if __name__ == "__main__":
    main()



