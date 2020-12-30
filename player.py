from node import Node
from max import MAX
import numpy as np
import copy
import time

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
            # value = -np.sum(clone)
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
        print("\nCalculating ...")
        start = time.time()
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
        print(f"Calculate done. Take {round(time.time() - start,2)}s\n")
        return bestMove.recentMove
