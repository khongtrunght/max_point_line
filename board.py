from max import MAX
import numpy as np
import random
import copy

class Board():
    """Simulate a board containing size x size spots."""
    MAX_VALUE = MAX.VALUE
    MAX_STEPS = MAX.STEPS

    def __init__(self, size):
        """Initialize board attributes."""
        self.size = size
        self.board = np.full((self.size, self.size), 0)
        self.buildBoard()
        self.valid_move = ["h" + str(i) for i in range(self.size)] + ["v" + str(i) for i in range(self.size)]
        self.steps = 0

    def buildBoard(self):
        """Build a board consisting of size x size spots in a grid."""
        for i in range(self.size):
            for j in range(self.size):
                self.board[i, j] = random.randint(-self.MAX_VALUE, self.MAX_VALUE)
        # DULIEUMAU = [[1,-6,7,-7,8,18],
        #     [-8,2,-4,-9,16,9],
        #     [14,-11,3,-10,-5,13],
        #     [10,17,-12,4,-1,-13],
        #     [-15,15,-2,-3,5,-14],
        #     [11,-16,12,-17,-18,6]]

        # self.board = np.array(DULIEUMAU)
        self.original_board = np.copy(self.board)

    def __str__(self):
        board_str = "\n"
        for i, row in enumerate(self.board):
            board_str += str(i) + " " 
            for number in row:
                if number < 0:
                    board_str += f"\033[34m{(-number): 3}\033[0m"
                elif number > 0:
                    board_str += f"\033[31m{number : 3}\033[0m"
                else:
                    board_str += f"{number : 3}"
            board_str += "\n"
        board_str += "\n  "
        for i in range(self.size):
            board_str += f"{i:3}"
        return board_str

    def choose_row(self, index):
        index = int(index)
        point = np.sum(self.board[index,:])
        self.board[index,:] = np.full(self.size,0)
        return point

    def choose_col(self, index):
        index = int(index)
        point = np.sum(self.board[:,index])
        self.board[:,index] = np.full(self.size,0)
        return point

    def getMoves(self):
        return copy.deepcopy(self.valid_move)

    def removeMove(self,move):
        try:
            self.valid_move.remove(move)
        except:
            print(f"{move} is not in valid moves")


    def applyMove(self, move):
        self.steps += 1
        self.removeMove(move)
        direction = move[0]
        index = move[1]
        if direction == 'h':
            new_point = self.choose_row(index)
        else:
            new_point = self.choose_col(index)
        return new_point

    def getSteps(self):
        return self.steps
