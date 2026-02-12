#!/usr/bin/env python3
from moves import State, Move, SearchNode
import heapq  # priority queue for A*
from itertools import count  # stable tie-breaking for the heap
import sys  # read command-line args + stdin


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
        sys.exit(1)  # exit as an error

    return n


'''
description: Receives a standard input from keyboard about the initial state of the large and small disks 
paramaters: 
return: State(large, small) , using the State class from moves.py 
'''
def initial_state_input(n):
    line1 = sys.stdin.readline()  # changed to stdin for redirected input as shown in lab
    line2 = sys.stdin.readline()

    if not line1 or not line2:
        raise ValueError("Expected two lines of input for large and small disk states.")

    large = list(map(int, line1.split()))  # list for large disk configuration
    small = list(map(int, line2.split()))  # list for small disk configuration

    if len(large) != n or len(small) != n:  # error checking
        raise ValueError(f"Expected {n} integers per line.")

    if 0 not in small:
        raise ValueError("Small disks must contain a 0.")

    return State(large, small)  # saved as a tuple as in the class State

# Just for testing
def initial_state_input_test():
    large = [1, 2, 2, 1, 3]
    small = [1, 1, 2, 2, 0]
    return State(large, small)


def do_move(state, move):
    """
    Apply Move(k, side) under the AB rules:

      - The blank (0) can swap with:
          * its adjacent disk (k = 1), OR
          * the disk k positions to the left/right,
            where k is the number shown on the uncovered large disk.

    The list is circular.
    Returns:
      - new State
    """
    obs = list(state.small)
    T = len(obs)
    blank = obs.index(0)

    k = move.k
    side = move.side

    if side == "R":
        src = (blank + k) % T
    else:
        src = (blank - k) % T

    obs[blank], obs[src] = obs[src], obs[blank]
    return State(state.large, obs)



def get_legal_moves(state):
    """
    If the uncovered large disk shows K, the only candidates are:

    Move(1, L/R) and Move(K, L/R)

    We allow do_move() to decide legality (returns None if impossible).
    """
    obs = state.small
    blank = obs.index(0)

    K = state.large[blank]     # value on the uncovered large disk
    candidates = set([1, K])   # avoid duplicates when K == 1

    moves = []
    for k in candidates:
        for side in ("L", "R"):
            moves.append(Move(k, side))

    return moves


def make_goal_pattern(initial_state):
    """
    Build the goal pattern from the instance:

    [1 repeated c1, 2 repeated c2, ..., m repeated cm, 0]

    where ci is how many i's appear in the starting small-disk list,
    and m is the max label.
    """
    obs = initial_state.small
    max_label = max(obs)

    counts = {}
    for v in obs:
        if v != 0:
            counts[v] = counts.get(v, 0) + 1

    goal = []
    for v in range(1, max_label + 1):
        goal.extend([v] * counts.get(v, 0))
    goal.append(0)

    return tuple(goal)


def rotate(state):
    """Rotate the small-disk list so that 0 becomes the last element.
    This allows easy comparison for the goal state up to rotation."""
    obs = state.small
    z = obs.index(0)
    return tuple(obs[z + 1 :] + obs[: z + 1])


def goal_reached(state, goal_tuple):
    """Goal check up to rotation: rotate so 0 is last, then compare."""
    return rotate(state) == goal_tuple


def astar_solve(start_state):
    """
    A* graph search.

    Heap ordering:
      1) smallest f = g + h
      2) if tie, prefer larger g (deeper)
      3) if still tie, FIFO by insertion order
    """
    goal_tuple = make_goal_pattern(start_state)

    # heap items are: (f, -g, order_id, SearchNode)
    # -g is used because heapq is a min-heap but we want ties broken by larger g
    heap = []
    order = count()

    # best g seen so far for each discovered state
    best_g = {}

    start_node = SearchNode(start_state, g=0, h=h(start_state), parent=None, move=None)
    heapq.heappush(heap, (start_node.f, -start_node.g, next(order), start_node))
    best_g[start_node.state] = 0

    while heap:
        _, _, _, node = heapq.heappop(heap)

        # checks for if a cheaper path was found after this was pushed
        if best_g.get(node.state, float("inf")) != node.g:
            continue

        # checks for goal
        if goal_reached(node.state, goal_tuple):
            return node

        for mv in get_legal_moves(node.state):
            nxt = do_move(node.state, mv)
            if nxt is None:
                continue

            g2 = node.g + 1
            old_g = best_g.get(nxt)

            # only keep strictly better routes
            if old_g is None or g2 < old_g:
                child = SearchNode(nxt, g=g2, h=h(nxt), parent=node, move=mv)
                best_g[nxt] = g2
                heapq.heappush(heap, (child.f, -child.g, next(order), child))

    return None


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
(eg. 1011 would not count a gap in the 1's)

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
    before_zero = obs[(zero_pos - 1) % T]

    prev = obs[(zero_pos + 1) % T]   # first value after 0 (nonzero)

    seen = {v: 0 for v in range(n + 1)}
    seen[prev] += 1

    h_val = 0
    first = True  # stays True until we leave the starting run

    # stop before we wrap back onto 0, so cur is never 0
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


def path_states(goal_node):
    """Collect the State objects from start -> goal."""
    out = []
    cur = goal_node
    while cur is not None:
        out.append(cur.state)
        cur = cur.parent
    out.reverse()
    return out


def print_solution(goal_node):
    """Print the solution path in the format the checker expects."""
    if goal_node is None:
        print("No solution")
        return

    print("Solution is")
    for st in path_states(goal_node):
        print(str(st))

# For the demo
def print_formatted_solution(goal_node):

    path = []
    current_node = goal_node

    while current_node:
        path.insert(0, current_node)
        current_node = current_node.parent

    arrow = ">"
    print("\n")
    for i in range(len(path) - 1):
        current_node = path[i]

        children = ""
        for move in get_legal_moves(current_node.state):
            current_node_children = do_move(current_node.state, move)

            if current_node_children is not None:
                children += f"  {str(current_node_children)}"

        print(f"{arrow}node: {current_node.state}")
        print(f"{arrow}children: {children} \n")

        arrow = "----" + arrow

    print(f"{arrow}solution node:{path[-1].state}")


'''
description: calls helper functions and prints the resulting solution of the puzzle 
paramaters: 
return: 
'''
def main():
    n = receive_n()
    start_state = initial_state_input(n)

    goal_node = astar_solve(start_state)
    print_solution(goal_node)

if __name__ == "__main__":
    main()
