
############################################################
# Imports
############################################################

import random
import copy
import Queue
import math

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = []
    for i in range(rows):
        row = []
        for j in range(1, cols + 1):
            row.append(i * cols + j)
        board.append(row)
    board[rows - 1][cols - 1] = 0
    return TilePuzzle(board)

class TilePuzzle(object):
    
    def __init__(self, board):
        self.board = board
        self.row_num = len(board)
        self.col_num = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        # get the index of 0-tile
        for row in range(self.row_num):
            if 0 in self.board[row]:
                col = self.board[row].index(0)
                break
        
        if direction == "up" and row > 0:
            temp_tile = self.board[row - 1][col]
            self.board[row - 1][col] = 0
            self.board[row][col] = temp_tile
            return True

        if direction == "down" and row < self.row_num - 1:
            temp_tile = self.board[row + 1][col]
            self.board[row + 1][col] = 0
            self.board[row][col] = temp_tile
            return True

        if direction == "left" and col > 0:
            temp_tile = self.board[row][col - 1]
            self.board[row][col - 1] = 0
            self.board[row][col] = temp_tile
            return True

        if direction == "right" and col < self.col_num - 1:
            temp_tile = self.board[row][col + 1]
            self.board[row][col + 1] = 0
            self.board[row][col] = temp_tile
            return True

        return False

    def scramble(self, num_moves):
        seq = ["up", "down", "left", "right"]
        for i in range(num_moves):
            self.perform_move(random.choice(seq))

    def is_solved(self):
        board = []
        for i in range(self.row_num):
            row = []
            for j in range(1, self.col_num + 1):
                row.append(i * self.col_num + j)
            board.append(row)
        board[self.row_num - 1][self.col_num - 1] = 0
        return self.board == board

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        for direction in ["up", "down", "left", "right"]:
            p = self.copy()
            if p.perform_move(direction):
                yield (direction, p)

    def iddfs_helper(self, limit, moves, trace):
        if len(moves) < limit:
            for (move, new_p) in self.successors():
                new_board = tuple(tuple(x) for x in new_p.board)
                if new_board not in trace:
                    new_trace = copy.deepcopy(trace)
                    new_trace.add(new_board)
                    for stuff in new_p.iddfs_helper(limit, moves + [move], new_trace):
                        yield stuff
        if self.is_solved():
            yield moves

    def find_solutions_iddfs(self):
        limit = 0
        solutions = []
        while len(solutions) == 0:
            solutions = list(self.iddfs_helper(limit, [], set(tuple(tuple(x) for x in self.board))))
            limit += 1
        for solution in solutions:
            yield solution

    def heuristic_md(self):
        heuristic = 0
        for i in range(self.row_num):
            for j in range(self.col_num):
                if self.board[i][j] != 0:
                    desired_row = (self.board[i][j] - 1) / self.col_num
                    desired_col = (self.board[i][j] - 1) % self.col_num
                    heuristic += abs(i - desired_row) + abs(j - desired_col)
        return heuristic

    def find_solution_a_star(self):
    '''solution to tile puzzle'''
        pq = Queue.PriorityQueue()
        pq.put((self.heuristic_md(), 0, [], self))  # add the initial state to queue
        trace = set()               # keep trace of board history
        while True:
            node = pq.get()         # expand according to priority
            if tuple(tuple(x) for x in node[3].board) in trace:     # discard the node if having been expanded
                continue
            else:
                trace.add(tuple(tuple(x) for x in node[3].board))   # add node to trace only when expanded
            if node[3].is_solved(): # optimal solution found
                return node[2]
            for (move, new_p) in node[3].successors():
                if tuple(tuple(x) for x in new_p.board) not in trace:
                    pq.put((node[1] + 1 + new_p.heuristic_md(), node[1] + 1, node[2] + [move], new_p))

############################################################
# Section 2: Grid Navigation
############################################################

class GridNavigation(object):

    def __init__(self, start, goal, scene):
        self.pos = start
        self.goal = goal
        self.scene = scene
        self.row_num = len(scene)
        self.col_num = len(scene[0])

    def perform_move(self, direction):
        if direction == "up" and self.pos[0] > 0 \
           and self.scene[self.pos[0] - 1][self.pos[1]] is False:
            self.pos = (self.pos[0] - 1, self.pos[1])
            return True

        if direction == "down" and self.pos[0] < self.row_num - 1 \
           and self.scene[self.pos[0] + 1][self.pos[1]] is False:
            self.pos = (self.pos[0] + 1, self.pos[1])
            return True

        if direction == "left" and self.pos[1] > 0 \
           and self.scene[self.pos[0]][self.pos[1] - 1] is False:
            self.pos = (self.pos[0], self.pos[1] - 1)
            return True

        if direction == "right" and self.pos[1] < self.col_num - 1 \
           and self.scene[self.pos[0]][self.pos[1] + 1] is False:
            self.pos = (self.pos[0], self.pos[1] + 1)
            return True

        if direction == "up-left" and self.pos[0] > 0 and self.pos[1] > 0 \
           and self.scene[self.pos[0] - 1][self.pos[1] - 1] is False:
            self.pos = (self.pos[0] - 1, self.pos[1] - 1)
            return True

        if direction == "up-right" and self.pos[0] > 0 and self.pos[1] < self.col_num - 1 \
           and self.scene[self.pos[0] - 1][self.pos[1] + 1] is False:
            self.pos = (self.pos[0] - 1, self.pos[1] + 1)
            return True

        if direction == "down-left" and self.pos[0] < self.row_num - 1 and self.pos[1] > 0 \
           and self.scene[self.pos[0] + 1][self.pos[1] - 1] is False:
            self.pos = (self.pos[0] + 1, self.pos[1] - 1)
            return True

        if direction == "down-right" and self.pos[0] < self.row_num - 1 and self.pos[1] < self.col_num - 1 \
           and self.scene[self.pos[0] + 1][self.pos[1] + 1] is False:
            self.pos = (self.pos[0] + 1, self.pos[1] + 1)
            return True        

        return False

    def is_solved(self):
        return self.pos == self.goal

    def copy(self):
        return GridNavigation(copy.deepcopy(self.pos), self.goal, self.scene)

    def successors(self):
        for direction in ["up", "down", "left", "right", "up-left", "up-right", "down-left", "down-right"]:
            p = self.copy()
            if p.perform_move(direction):
                yield (direction, p.pos, p)

    def heuristic_ed(self):
        return math.sqrt((self.pos[0] - self.goal[0]) ** 2 + (self.pos[1] - self.goal[1]) ** 2)

    def find_path_a_star(self):
    '''solution to grid navigation'''
        if self.scene[self.pos[0]][self.pos[1]]:    # start at obstacle
            return None
        pq = Queue.PriorityQueue()
        pq.put((self.heuristic_ed(), 0, [self.pos], self))      # add the initial state to queue
        trace = set()               # keep trace of pos history
        while True:
            if pq.empty():          # no optimal solution
                return None
            node = pq.get()         # expand according to priority
            if node[3].pos in trace:    # discard the node if having been expanded
                continue
            else:
                trace.add(node[3].pos)  # add node.pos to trace only when firstly expanded
            if node[3].is_solved(): # optimal solution found
                return node[2]
            for (direction, new_pos, new_p) in node[3].successors():
                if new_pos not in trace:    # don't add to the queue if the node has been expanded
                    if direction in ["up", "down", "left", "right"]:    # step cost = 1
                        pq.put((node[1] + 1 + new_p.heuristic_ed(), node[1] + 1, node[2] + [new_pos], new_p))
                    else:           # step cost = sqrt(2)
                        pq.put((node[1] + math.sqrt(2) + new_p.heuristic_ed(), \
                                node[1] + math.sqrt(2), node[2] + [new_pos], new_p))

def find_path(start, goal, scene):
    p = GridNavigation(start, goal, scene)
    return p.find_path_a_star()

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

class solve_disks(object):
    
    def __init__(self, length, n, grid):    # usually grid = 0 or [] when initialzing
        self.length = length
        self.n = n
        if grid == 0 or len(grid) == 0:
            self.grid = range(n) + [-1] * (length - n)
        elif len(grid) == length:
            self.grid = grid
        else:
            return

    def perform_move(self, i, steps):
        if (i + steps) < 0 or (i + steps) >= self.length:
            return
        self.grid[i + steps] = self.grid[i]     # steps = -2, -1, 1, 2
        self.grid[i] = -1

    def is_solved(self):
        for i in range(self.length - self.n):
            if self.grid[i] != -1:
                return False
        for i in range(self.length - self.n, self.length):
            if self.grid[i] != self.length - i - 1:
                return False
        return True

    def copy(self):
        return solve_disks(self.length, self.n, copy.deepcopy(self.grid))

    def successors(self):
        for i in range(self.length):
            if (self.grid[i] != -1 and (i + 1) < self.length \
                and self.grid[i + 1] == -1):
                d = self.copy()
                d.perform_move(i, 1)
                yield (i, i + 1), d
                
            if (self.grid[i] != -1 and (i + 2) < self.length \
                and self.grid[i + 1] != -1 and self.grid[i + 2] == -1):
                d = self.copy()
                d.perform_move(i, 2)
                yield (i, i + 2), d
                
            if (self.grid[i] != -1 and (i - 1) >= 0 \
                and self.grid[i - 1] == -1):
                d = self.copy()
                d.perform_move(i, -1)
                yield (i, i - 1), d
                
            if (self.grid[i] != -1 and (i - 2) >= 0 \
                and self.grid[i - 1] != -1 and self.grid[i - 2] == -1):
                d = self.copy()
                d.perform_move(i, -2)
                yield (i, i - 2), d

    def heuristic(self):
        heuristic = 0
        for i in range(self.length):
            if self.grid[i] != -1:
                heuristic += abs(self.length - 1 - self.grid[i] - i)
        return heuristic

    def find_solution_a_star(self):
    '''solution to distinct disk problem'''
        pq = Queue.PriorityQueue()
        pq.put((self.heuristic(), 0, [], self))  # add the initial state to queue
        trace = set()               # keep trace of pos history
        while True:
            if pq.empty():          # no optimal solution
                return None
            node = pq.get()         # expand according to priority
            if tuple(node[3].grid) in trace:    # discard the node if having been expanded
                continue
            else:
                trace.add(tuple(node[3].grid))  # add node to trace only when expanded
            if node[3].is_solved(): # optimal solution found
                return node[2]
            for (move, new_p) in node[3].successors():
                if tuple(new_p.grid) not in trace:
                    pq.put((node[1] + 1 + new_p.heuristic(), node[1] + 1, node[2] + [move], new_p))

def solve_distinct_disks(length, n):
    p = solve_disks(length, n, 0)
    return p.find_solution_a_star()
