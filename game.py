from board import Board
from max import MAX
import copy


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

        # if (p1.isRedSide()):
        #     self.currentTurn = p1
        # else:
        #     self.currentTurn = p2
        
        

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
        # print(f"\n Point: \033[31mHuman: {self.players['human'].getPoint()}\033[34m  Ai: {self.players['ai'].getPoint()}\033[0m")
        print(f"{self.players['human']} {self.players['ai']}")
    def applyMove(self, move, player):
        self.currentTurn = 1 - self.currentTurn
        new_point = self.board.applyMove(move)
        if player.isRedSide():
            player.updatePoint(new_point) 
        else:
            player.updatePoint(-new_point)

    def getMoves(self):
        return self.board.getMoves()

