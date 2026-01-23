'''
the linked lists OOP for the tile moves of n, saving visited states, 
A* frontier (a priority queue)
- class Node 
    - class State -> what we search for 
    - class Move -> how the tile gets there 
    - g,h,f
    - parent -> initial configuration 

- class LinkedList - shows final path 
- every legal action is represented as Move(k, side) where k is either 1 or the uncovered large disk value, and side is left or right.”

'''
class SearchNode: 
    def __init__(self, state, g, h, parent=None, move=None):
        self.state = state      # State object
        self.g = g              # cost so far
        self.h = h              # heuristic
        self.f = g + h          # priority value for A*
        self.parent = parent    # previous SearchNode
        self.move = move        # Move used to get here

# ONLY for printing the final solution (ListNode and Linked List)

class ListNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        new_node = ListNode(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield cur.value
            cur = cur.next

# Move - (for information)
class Move: 
    """
    Represents a single legal move in the puzzle.

    A move is defined by:
      - k: which smaller disk to move
            * k = 1  → first smaller disk in the chosen direction
            * k > 1  → k-th smaller disk in the chosen direction
            * k is either 1 or the number shown on the uncovered large disk

      - side: direction to search in the circular arrangement
            * "L" → search to the left (counter-clockwise)
            * "R" → search to the right (clockwise)

    NOTE:
    This class does NOT change the state.
    It only stores the information needed so the search algorithm
    can later apply the move to a state.
    """
    def __init__(self, k, side): 
        """
        Make a new move.

        Parameters:
        ----------
        k : int
            The index (count) of the smaller disk to select.
            Example:
              k = 1 → first smaller disk
              k = 3 → third smaller disk

        side : str
            Direction to search in the circle.
            Must be either:
              "L" → left (counter-clockwise)
              "R" → right (clockwise)
        """
        if side not in ("L", "R"):
            raise ValueError("side must be 'L' or 'R'")
        
        self.k = k # 1 or uncovered large disk number 
        self.side = side # 'L' or 'R' (left or right)

    def __str__(self):
        """
        Convert the move to a readable string.

        Example outputs:
          "1-from-left"
          "3-from-right"
        """
        return f"{self.k}-from-{'left' if self.side == 'L' else 'right'}"
    
    def __eq__(self, other):
        """
        Check if two Move objects are equal.

        Two moves are considered equal if:
          - they move the same k-th smaller disk
          - in the same direction

        This allows Move objects to be compared safely,
        which is useful for testing and debugging.
        """
        return isinstance(other, Move) and self.k == other.k and self.side == other.side

    def __hash__(self):
        """
        Return a hash value for the move.

        This allows Move objects to be:
          - stored in sets
          - used as dictionary keys

        Hashing is based on (k, side),
        since those two values fully define a move.
        """
        return hash((self.k, self.side))
    
# searching each visited state 
'''
A single configuration, the State object shows: 
- fixed arrangemnet of large disks 
- current arrangemnet of smaller disks 
'''
class State:
    def __init__(self, large, small):
        '''
        tuple of the current large and small arrangements of disks 
        '''
        self.large = tuple(large)
        self.small = tuple(small)

    def __eq__(self, other):
        '''
        For comparing states to each other: 
        - other visited states 
        - or duplicated states 
        '''
        return isinstance(other, State) and self.small == other.small
    
    def __str__(self):
        """
        Print the small disk configuration in the required output format.
        """
        return " ".join(str(x) for x in self.small)
    
    # for debugging, checking the large tile configuration
    def debug_str(self):
        return f"Large: {self.large}\nSmall: {self.small}"

    def __hash__(self):
        '''
        allows State objects to be: 
        - stores in a set 
        - as dictinary keys (for best cost)
        '''
        return hash(self.small)


