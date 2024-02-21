# Game playing framework for CSE3300
#
# (c)2021 W. Boehmer <j.w.bohmer@tudelft.nl>

from math import ceil
import numpy as np
from copy import deepcopy


##############################################################################

class Action:
    def __init__(self, player, x):
        self.player = player
        self.x = x

    def __str__(self):        # to look better
        return str(self.x)

    def __eq__(self, other):  # for comparisons (`if a in list`)
        return self.player == other.player and self.x == other.x

    def __hash__(self):       # for use in dictionaries (hash maps)
        return hash((self.player, self.x))


class State:
    def __init__(self, player=1):
        self.player = player        # $p(s) \in \{-1,1\}$

    def actions(self):              # $\mathcal A(s)$
        return []    # list of legal actions

    def transition(self, action):   # $\mathcal P(s,a) \in \mathcal S$
        return None  # new state after action

    def terminal(self):             # $\mathcal T(s) \in \{\top, \bot\}$
        return None  # boolean whether the game ends

    def reward(self):               # $\mathcal R(s) \in \mathbb R$
        return None  # 1 for won, 0 for draw and -1 for lost


class Heuristic:
    def heuristic(self, action=None):  # value heuristic for state (action is None) or relative value of action
        return None                    # returns a real number


##############################################################################

# OXO: see https://en.wikipedia.org/wiki/Tic-tac-toe

class NoughtsAndCrosses(State, Heuristic):
    class Action(Action):
        def __init__(self, player, x, y):
            super().__init__(player, x)
            self.y = y

        def __str__(self):
            return str((self.x, self.y))

        def __eq__(self, other):
            return super().__eq__(other) and self.y == other.y

        def __hash__(self):
            return hash((self.x, self.y, self.player))

    def __init__(self, size):
        super().__init__(player=1)
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def __str__(self):  # to look nice
        s = ''
        for row in self.board:
            for c in row:
                s += '|x' if c == 1 else '|o' if c == -1 else '| '
            s += '|\n'
        return s

    def actions(self):  # $\mathcal A(s)$
        possible_actions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    possible_actions.append(NoughtsAndCrosses.Action(player=self.player, x=i, y=j))
        return possible_actions

    def transition(self, action):  # $\mathcal P(s,a) \in \mathcal S$
        state = deepcopy(self)
        state.board[action.x][action.y] = action.player
        state.player *= -1
        return state

    def reward(self):  # $\mathcal R(s) \in \mathbb R$
        for row in self.board:
            if abs(sum(row)) == self.size:
                return sum(row) / self.size
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == self.size:
                return sum(column) / self.size
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == self.size:
                return sum(diagonal) / self.size
        return False

    def terminal(self):  # $\mathcal T(s) \in \{\top, \bot\}$
        return self.reward() != 0 or len(self.actions()) == 0

    def _middle(self, i, j):
        n = self.size
        return 1 if (i == n // 2 or i == ceil(n / 2)) and (j == n // 2 or j == ceil(n / 2)) else 0
    
    def _corner(self, i, j):
        n = self.size
        return 1 if (i == 0 or i == (n - 1)) and (j == 0 or j == (n - 1)) else 0

    def heuristic(self, action=None):
        if action is None:  # value-heuristic of the current state
            value = 0
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    value += self.board[i][j] * (2 * self._middle(i, j) + self._corner(i, j))
            return value / 2 / self.size / self.size
        else:  # value-heuristic of the given action (relative to current state)
            return self.player * (2 * self._middle(action.x, action.y) + self._corner(action.x, action.y))


## American English: "tic tac toe"        
TicTacToe = NoughtsAndCrosses(3)


##############################################################################

# DnB: see https://en.wikipedia.org/wiki/Dots_and_Boxes

class DotsAndBoxes(State, Heuristic):
    class Action(Action):
        def __init__(self, player, x, y, h):
            super().__init__(player, x)  # player and x position of edge
            self.y = y  # y position of the edge
            self.h = h  # whether the edge is horizontal (1) or vertical (0)

        def __str__(self):
            return str((self.h, self.x, self.y))

        def __eq__(self, other):
            return super().__eq__(other) and self.y == other.y and self.h == other.h

        def __hash__(self):
            return hash((self.h, self.x, self.y, self.player))

    def __init__(self, width, height):
        super().__init__(player=1)
        self.width = width
        self.height = height
        # board: vertical/horizontal, y-axis, x-axis
        self.board = [[[0 for _ in range(width + 1)] for _ in range(height)],
                      [[0 for _ in range(width)] for _ in range(height + 1)]]
        self.boxes = [[' ' for _ in range(width)] for _ in range(height)]
        # state also depends on previously won boxes, i.e. points
        self.points = 0

    def __str__(self):
        s = ''
        for y in range(self.height + 1):
            # Horizontal edges
            for x in range(self.width):
                s += 'o---' if self.board[1][y][x] != 0 else 'o   '
            s += 'o\n'
            # Vertical edges
            if y < self.height:
                for x in range(self.width + 1):
                    s += '|' if self.board[0][y][x] != 0 else ' '
                    s += '' if x == self.width else ' ' + self.boxes[y][x] + ' '
                s += '\n'
        return s
    def actions(self):  # $\mathcal A(s)$
        possible_actions = []
        vertical = self.board[0]
        horizontal = self.board[1]

        width = len(vertical[0])
        height = len(vertical)
        #import ipdb;ipdb.set_trace()

        for y in range(height):
            for x in range(width):
                if vertical[y][x] == 0:
                    possible_actions.append(DotsAndBoxes.Action(player=self.player, x=x, y=y, h=0))

        for y in range(height+1):
            for x in range(width-1):
                if horizontal[y][x] == 0:
                    possible_actions.append(DotsAndBoxes.Action(player=self.player, x=x, y=y, h=1))

        return possible_actions

    def check_box(self, x: int, y: int) -> bool:
        if x<0 or y<0:
            return False

        try:
            res = True
            res &= self.board[0][y][x] != 0
            res &= self.board[1][y][x] != 0
            res &= self.board[0][y][x+1] != 0
            res &= self.board[1][y+1][x] != 0
            return res
        except IndexError:
            return False

    def transition(self, action):  # $\mathcal P(s,a) \in \mathcal S$
        state = deepcopy(self)
        x = action.x
        y = action.y
        state.board[action.h][action.y][action.x] = action.player
        b1 = state.check_box(x, y)
        b2 = False
        if b1:
            state.boxes[y][x] = str(state.player)[0]
        if action.h == 0:
            if (b2 := state.check_box(x-1, y)):
                state.boxes[y][x-1] = str(state.player)[0]
        else:
            if (b2 := state.check_box(x, y-1)):
                state.boxes[y-1][x] = str(state.player)[0]
        
        if b1 or b2:
            state.points+=(int(b1)+int(b2))*state.player
        else:
            state.player *= -1
        return state

    def reward(self) -> int:
        return self.points

    def terminal(self) -> bool:
        return len(self.actions()) == 0


