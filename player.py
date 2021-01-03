from node import Node
from max import MAX
import numpy as np
import copy
import time

class Player():
    red = "\033[31m"
    blue = "\033[34m"
    MAX_STEPS = MAX.STEPS
    """Simulate one of the participants playing the game."""
    def __init__(self, redSide):
        self.point = 0
        self.redSide = redSide
        if self.redSide:
            self.color = self.red
        else:
            self.color = self.blue

    def updatePoint(self,new_point):
        self.point += new_point

    def isRedSide(self):
        return self.redSide

    def isHumanPlayer(self):
        return self.humanPlayer

    def getPoint(self):
        return self.point
    
    def __str__(self):
        string = ""
        if self.isRedSide():
            string += "\033[31m"#Human: {self.players['human'].getPoint()}\033["
        else:
            string += "\033[34m"

        string += f"{self.name}: "
        # if self.isHumanPlayer():
        #     string += "Human: "
        # else:
        #     string += "AI: "

        string += f"{self.getPoint()} \033[0m"

        return string

        



class HumanPlayer(Player):
    def __init__(self,name, redSide):  # redSide play first
        super().__init__(redSide)
        self.humanPlayer = True
        self.name = name


class AIPlayer(Player):
    def __init__(self,name, redSide):  # redSide play first
        super().__init__(redSide)
        self.humanPlayer = False
        self.name = name
        
    def getMoves(self, board):
        possibleMoves = []

        for move in board.getMoves():
            clone = copy.deepcopy(board)
            clone.applyMove(move)
            # value = -np.sum(clone)
            node = Node(clone, move)
            possibleMoves.append(node)

        return possibleMoves
        

    def minimax(self, node, currentSteps = 0, isMaximized = False, global_depth = 0 ):
        currentSteps += 1
        if currentSteps == MAX.STEPS + 1:
            node.value = np.sum(node.states.original_board - node.states.board)
            # node.value = -np.sum(node.states.board)
            return node.value

        if not isMaximized:
            # min player's turn 
            return min([self.minimax(cnode, currentSteps, True, global_depth) for cnode in self.getMoves(node.states)])
        else:
            # max player's turn
            return max([self.minimax(cnode, currentSteps, False, global_depth) for cnode in self.getMoves(node.states)])

    def makeMove(self, board, isMaximized = False):
        print("\nCalculating ...")
        start = time.time()
        possibleMoves = self.getMoves(board)
        if not isMaximized:
            for move in possibleMoves:
                move.value = self.minimax(move,board.getSteps()+1,True, board.getSteps() + 1) 
            bestMove = possibleMoves[0]
            for move in possibleMoves:
                if move.value < bestMove.value:
                    bestMove = move
        else:
            for move in possibleMoves:
                move.value = self.minimax(move,board.getSteps()+1,False, board.getSteps() + 1)
            bestMove = possibleMoves[0]
            for move in possibleMoves:
                if move.value > bestMove.value:
                    bestMove = move
        print(f"Calculate done. Take {round(time.time() - start,2)}s\n")
        return bestMove.recentMove


class GreedyAIPlayer(AIPlayer):
    def makeMove(self, boardOBJ, isMaximized = False):
        board = boardOBJ.board
        print("\nCalculating ...")
        start = time.time()
        possibleMoves = self.getMoves(boardOBJ)
        if not isMaximized:
            max_value = float('inf')
            for node in possibleMoves:
                move = node.recentMove
                if move[0] == 'h':
                    if max_value > np.sum(board[int(move[1]),:]):
                        max_value = np.sum(board[int(move[1]),:])
                        bestMove = node
                else:
                    if max_value > np.sum(board[:,int(move[1])]):
                        max_value = np.sum(board[:, int(move[1])])
                        bestMove = node
        else:
            max_value = -float('inf')

            for node in possibleMoves:
                move = node.recentMove
                if move[0] == 'h':
                    if max_value < np.sum(board[int(move[1]), :]):
                        max_value = np.sum(board[int(move[1]), :])
                        bestMove = node
                else:
                    if max_value < np.sum(board[:, int(move[1])]):
                        max_value = np.sum(board[:, int(move[1])])
                        bestMove = node

        print(f"Calculate done. Take {round(time.time() - start, 2)}s\n")
        return bestMove.recentMove


class ABAIPlayer(AIPlayer):
    def AlphaBeta(self, node,a,b, currentSteps=0,isMaximized=False):
        currentSteps += 1
        if currentSteps == MAX.STEPS + 1:
            node.value = np.sum(node.states.original_board - node.states.board)
            # node.value = -np.sum(node.states.board)
            return node.value

        if not isMaximized:
            # min player's turn
            for cnode in self.getMoves(node.states):
                tmp = self.AlphaBeta(cnode,a,b, currentSteps, True)
                b = min(tmp,b)
                if a>= b:
                    break
            return b
        else:
            # max player's turn
            for cnode in self.getMoves(node.states):
                tmp = self.AlphaBeta(cnode,a,b, currentSteps, False)
                a = max(tmp,a)
                if a>=b:
                    break
            return a

    def minimax(self,node,currentSteps=0,isMaximized=False, global_depth = 0):
        return self.AlphaBeta(node,-100,100, currentSteps,isMaximized, global_depth = global_depth)

class LimitAIPlayer(ABAIPlayer):
    def AlphaBeta(self, node,a,b, currentSteps=0,isMaximized=False, global_depth = 0):
        
        limit_search_steps = ((MAX.SEARCH_LIMIT + global_depth) // 2) * 2
        if currentSteps == min(MAX.STEPS , limit_search_steps ):
            node.value = np.sum(node.states.original_board - node.states.board)
            # node.value = -np.sum(node.states.board)
            return node.value

        currentSteps += 1

        if not isMaximized:
            # min player's turn
            for cnode in self.getMoves(node.states):
                tmp = self.AlphaBeta(cnode,a,b, currentSteps, True, global_depth)
                b = min(tmp,b)
                if a>= b:
                    break
            return b
        else:
            # max player's turn
            for cnode in self.getMoves(node.states):
                tmp = self.AlphaBeta(cnode,a,b, currentSteps, False, global_depth)
                a = max(tmp,a)
                if a>=b:
                    break
            return a
    
    def minimax(self,node,currentSteps=0,isMaximized=False, global_depth = 0):
        return self.AlphaBeta(node,-100,100, currentSteps,isMaximized, global_depth = global_depth) 
