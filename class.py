import numpy as np
import random
import copy
import time


class Node():
    def __init__(self, states = None, recentMove = None, value = None):
        self.states = states
        self.recentMove = recentMove
        self.value = value

class MAX():
    STEPS = 4
    SIZE = 6
    VALUE = 9

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
            Print(f"{move} is not in valid moves")


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


class Player():
    MAX_STEPS = MAX.STEPS
    """Simulate one of the participants playing the game."""
    def __init__(self):
        self.point = 0
    def updatePoint(self,new_point):
        self.point += new_point

    def isRedSide(self):
        return self.redSide

    def isHumanPlayer(self):
        return self.humanPlayer

    def getPoint(self):
        return self.point
    



class HumanPlayer(Player):
    def __init__(self, redSide):  # redSide play first
        super().__init__()
        self.redSide = redSide
        self.humanPlayer = True


class AIPlayer(Player):
    def __init__(self, redSide):  # redSide play first
        super().__init__()
        self.redSide = redSide
        self.humanPlayer = False

    def getMoves(self, board):
        possibleMoves = []

        for move in board.getMoves():
            clone = copy.deepcopy(board)
            clone.applyMove(move)
            node = Node(clone, move)
            possibleMoves.append(node)

        return possibleMoves
        




    def ab_make_move(self, game):
        return game.getMoves()[0]

    def minimax(self, node, currentSteps = 0, isMaximized = False):
        currentSteps += 1
        if currentSteps == MAX.STEPS + 1:
            node.value = np.sum(node.states.original_board - node.states.board)
            # node.value = -np.sum(node.states.board)
            return node.value

        if not isMaximized:
            # min player's turn 
            return min([self.minimax(cnode, currentSteps, True) for cnode in self.getMoves(node.states)])
        else:
            # max player's turn
            return max([self.minimax(cnode, currentSteps, False) for cnode in self.getMoves(node.states)])

    def makeMove(self, board, isMaximized = False):
        possibleMoves = self.getMoves(board)
        if not isMaximized:
            for move in possibleMoves:
                move.value = self.minimax(move,board.getSteps()+1,True)
            bestMove = possibleMoves[0]
            for move in possibleMoves:
                if move.value < bestMove.value:
                    bestMove = move
        else:
            for move in possibleMoves:
                move.value = self.minimax(move,board.getSteps()+1,False)
            bestMove = possibleMoves[0]
            for move in possibleMoves:
                if move.value > bestMove.value:
                    bestMove = move
        return bestMove.recentMove


class Game():
    """Visualize the board and control the flow of the game."""
    MAX_STEPS = MAX.STEPS
    SIZE = MAX.SIZE
    turn = ["human",'ai']
    def __init__(self, human, ai):
        self.board = Board(self.SIZE)
        self.players = {"human": human, "ai": ai}
        self.currentTurn = 0
        self.board.buildBoard()
        
        

        # movesPlayed = []
    def getCurrentTurn(self):
        return self.players[self.turn[self.currentTurn]]
    def isEnd(self):
        return self.getSteps() == self.MAX_STEPS

    def getSteps(self):
        return self.board.getSteps()
    def getStatus(self):
        if self.players["human"].getPoint() > self.players["ai"].getPoint():
            self.status = "You Win !!!"
        elif self.players["human"].getPoint() < self.players["ai"].getPoint():
            self.status = "You Lost !!!"
        else:
            self.status = "It's a tie !!!"
        return self.status

    def getBoard(self):
        return copy.deepcopy(self.board)

    def printBoard(self):
        print(str(self.board))
        print(f"\n Point: \033[31mHuman: {self.players['human'].getPoint()}\033[34m  Ai: {self.players['ai'].getPoint()}\033[0m")

    def applyMove(self, move, player):
        self.currentTurn = 1 - self.currentTurn
        new_point = self.board.applyMove(move)
        if player.isHumanPlayer():
            player.updatePoint(new_point) 
        else:
            player.updatePoint(-new_point)

    def getMoves(self):
        return self.board.getMoves()



def main():
    
    print("\033[94m===================================================================\033[0m\033[22m")
    print(
        "\nWelcome! To play, enter a command, e.g. '\033[95mh3\033[0m'. 'h' for horizontal and 'v' for vertical.")
    human = HumanPlayer(redSide=True)
    ai = AIPlayer(redSide=False)
    game = Game(human, ai)
    game.printBoard()
    while not game.isEnd():
        user_move = input("\n Make a move: \033[31m")
        print("\033[0m")
        while user_move not in game.getMoves():
            user_move = input("Please enter a valid move: ")
        game.applyMove(user_move, human)
        game.printBoard()
        if not game.isEnd():
            start = time.time()
            computer_move = ai.makeMove(game.getBoard())
            print(f"Thoi gian: {time.time() - start}")
            game.applyMove(computer_move, ai)
            print(f"AI choose \033[34m{str(computer_move)}\033[0m")
            game.printBoard()
    print("Result: " + game.getStatus())
main()


# human = HumanPlayer(redSide=True)
# ai = AIPlayer(redSide=False)
# game = Game(human, ai)
# game.printBoard()
# game.applyMove("h3", human)
# # game.applyMove("v3",ai)
# # # game.applyMove("h0", human)
# # # game.applyMove("v2",ai)
# print(ai.minimax(Node(game.board),1,False))
# print(ai.makeMove(game.board,False))