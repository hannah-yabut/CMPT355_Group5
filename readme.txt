# CMPT355_Group5
Project 1 

# AB Puzzle Solver (A* Search)
  This program solves instances of the AB puzzle using A* graph search. 

# The puzzle consists of:
  - A fixed circular arrangement of large disks
  - A circular arrangement of small disks where '0' indicates the uncovered large disk.

----------------------------------------------------------------
# Directory Structure
----------------------------------------------------------------

AB.py
    Main program file.
    - Handles command-line argument parsing
    - Reads input from standard input
    - Implements A* search algorithm
    - Contains heuristic function
    - Prints solution in required format

moves.py
    Contains object-oriented classes used by the solver:
    - State (represents a configuration)
    - Move (represents a legal move)
    - SearchNode (used by A*)
    - Linked list structures for path tracking

Makefile
    Generates executable file named "AB"
    Includes lint and clean targets.

readme.txt
    Instructions for compiling and running the program.

report.pdf
    A short description of the search algorithm.

----------------------------------------------------------------
# Compilation Instructions:
----------------------------------------------------------------

The program is written in Python 3. 

To generate the executable file, run: make

This creates an executable file named: AB

To check syntax, run: make lint

To remove generated files, run: make clean


----------------------------------------------------------------
Execution Instructions
----------------------------------------------------------------

Run the program as: ./AB n

Where n is the number of disks.

Example:

    ./AB 10

After running the program, enter two lines of input
from the keyboard (standard input):

Line 1:
    Large disk numbers (space-separated integers)

Line 2:
    Small disk numbers (space-separated integers)
    One value must be 0 (represents uncovered disk)

The output will be printed to standard output.

----------------------------------------------------------------
Search Algorithm
----------------------------------------------------------------

- The program uses the A* search algorithm to solve the AB puzzle.

- Each state represents a configuration of the small disks.

- States are prioritized using f(n) = g(n) + h(n), where g is the move      count and h is a gap-based heuristic.

- A priority queue selects the lowest-cost state, with tie-breaking         favoring deeper nodes.

- Visited states are stored to avoid revisiting configurations and ensure   optimality.  
