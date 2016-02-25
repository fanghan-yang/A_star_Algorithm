# A_star_Algorithm
Tile Puzzle / Grid Navigation / Linear Disk Movement solved by A* Algorithm

Tile Puzzle: (A* or IDDFS)

The calssical Eight Puzzle consists of a 3×3 board of sliding tiles with a single empty space. For each configuration, 
the only possible moves are to swap the empty tile with one of its neighboring tiles. The goal state for the puzzle 
consists of tiles 1-3 in the top row, tiles 4-6 in the middle row, and tiles 7 and 8 in the bottom row, with the empty 
space in the lower-right corner. My code is more than Eight Puzzle, it can be any size of board you like.

You can play with an interactive version of the Tile Puzzle using GUI by running the following command line:

    python tile_puzzle_gui.py rows cols

(where the arguments rows and cols are positive integers designating the size of the puzzle)

Eg.

    python tile_puzzle_gui.py 3 3

    python tile_puzzle_gui.py 4 5

Note that the timing for two algorithms:

    A* search: Solve any 3x3 board fast, as well as simple scrambles on larger boards.

    IDDFS: solve scrambles of 10 moves or fewer on a 3x3 board in a couple seconds.

    Scramble normally produce a pattern requiring a solution of 15 to 25 moves.
    
    
Grid Navigation: (A* Algorithm)

The goal is of grid navigation is to produce the shortest path between a provided pair of points, taking care 
to maneuver around the obstacles as needed. Path length is measured in Euclidean distance. Valid directions of 
movement include up, down, left, right, up-left, up-right, down-left, and down-right.

You can visualize the paths it produces using GUI by running the following command line:

    python grid_navigation_gui.py scene_path
    
(the argument "scene_path" is a path to a scene file storing the layout of the target grid 
and obstacles. I use the following format for textual scene representation: "." characters 
correspond to empty spaces, and "X" characters correspond to obstacles. I provide three
scenes: simple_scene / barrier_scene / random_scene)

Eg.

    python grid_navigation_gui.py simple_scene
    
    python grid_navigation_gui.py barrier_scene
    
    python grid_navigation_gui.py random_scene
    
    
Linear Disk Movement: (A* Algorithm)

The starting configuration of this puzzle is a row of l cells, with disks located on cells 0 through n−1. The goal 
is to move the disks to the end of the row using a constrained set of actions. At each step, a disk can only be 
moved to an adjacent empty cell, or to an empty cell two spaces away, provided another disk is located on the 
intervening square.

Eg.

    solve_distinct_disks(15, 7)

    solve_distinct_disks(20, 9)

