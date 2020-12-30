import numpy as np
from board import Board
from player import HumanPlayer, AIPlayer
from game import Game
import time


class GameController():
    def runGame(self):
        while True:
            print("\033[94m===================================================================\033[0m\033[22m")
            control = input("Do you want to play first: (y/n)? ")
            if control == "y":
                self.human = HumanPlayer(redSide=True)
                self.ai = AIPlayer(redSide=False)
                self.redSide = self.human
            else:
                self.human = HumanPlayer(redSide= False)
                self.ai = AIPlayer(redSide=True)
                self.redSide = self.ai
            self.game = Game(self.human, self.ai)
            self.game.printBoard()
            print("\nWelcome! To play, enter a command, e.g. '\033[95mh3\033[0m'. 'h' for horizontal and 'v' for vertical.")
            while not self.game.isEnd():
                self.redSideMove()
                if not self.game.isEnd():
                    self.notRedSideMove()
                    if self.game.isEnd():
                        self.printResult()
                    continue
                else:
                    self.printResult()
                
                
                    
                    
            
    
    def redSideMove(self):
        if self.redSide.isHumanPlayer():
            user_move = input("\n Make a move: \033[31m")
            print("\033[0m")
            while user_move not in self.game.getMoves():
                user_move = input("Please enter a valid move: ")
            self.game.applyMove(user_move, self.human)
            self.game.printBoard()
        else:
            computer_move = self.ai.makeMove(self.game.getBoard())
            # print(f"Thoi gian: {time.time() - start}")
            self.game.applyMove(computer_move, self.ai)
            print(f"AI choose \033[34m{str(computer_move)}\033[0m")
            self.game.printBoard()

    def notRedSideMove(self):
        if not self.redSide.isHumanPlayer():
            user_move = input("\n Make a move: \033[31m")
            print("\033[0m")
            while user_move not in self.game.getMoves():
                user_move = input("Please enter a valid move: ")
            self.game.applyMove(user_move, self.human)
            self.game.printBoard()
        else:
            computer_move = self.ai.makeMove(self.game.getBoard())
            # print(f"Thoi gian: {time.time() - start}")
            self.game.applyMove(computer_move, self.ai)
            print(f"AI choose \033[34m{str(computer_move)}\033[0m")
            self.game.printBoard()
        
        

    def printResult(self):
        print("Result: " + self.game.getStatus())
        control = input("Do you want to continue? (y/n) ")
        if control == "y":
            self.runGame()
        else:
            exit()


        

def main():
    gameController = GameController()
    gameController.runGame()

main()