import numpy as np
from board import Board
from player import HumanPlayer, AIPlayer, ABAIPlayer, GreedyAIPlayer, LimitAIPlayer
from game import Game
import time


class GameController():
    
    def __init__(self):
        self.mode = {'2': self.humanVsBot, '1': self.botVsbot}
        print("\033[94m===================================================================\033[0m\033[22m")
        self.control = input("Please select mode: \n\t1, Bot Vs Bot\n\t2, Human vs Bot\n")
        self.mode[self.control]()

    def humanVsBot(self):
        while True:
            print("\033[94m===================================================================\033[0m\033[22m")
            control = input("Do you want to play first: (y/n)? ")
            if control == "y":
                self.redSide = HumanPlayer("Tuan",redSide=True)
                self.notRedSide = AIPlayer("AI",redSide=False)
            else:
                self.redSide = AIPlayer("AI",redSide=True)
                self.notRedSide = HumanPlayer("Tuan",redSide= False)
            self.game = Game(self.redSide, self.notRedSide)
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
                
    def botVsbot(self):
        self.redSide = LimitAIPlayer("BOT limit", redSide = True)
        self.notRedSide = AIPlayer("BOT mini", redSide = False)
        self.game = Game(self.redSide, self.notRedSide)
        self.game.printBoard()
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
            self.game.applyMove(user_move, self.redSide)
            self.game.printBoard()
        else:
            computer_move = self.redSide.makeMove(self.game.getBoard(), True)
            # print(f"Thoi gian: {time.time() - start}")
            self.game.applyMove(computer_move, self.redSide)
            print(f"{self.redSide.name} choose \033[31m{str(computer_move)}\033[0m")
            self.game.printBoard()

    def notRedSideMove(self):
        if self.notRedSide.isHumanPlayer():
            user_move = input("\n Make a move: \033[34m")
            print("\033[0m")
            while user_move not in self.game.getMoves():
                user_move = input("Please enter a valid move: ")
            self.game.applyMove(user_move, self.notRedSide)
            self.game.printBoard()
        else:
            computer_move = self.notRedSide.makeMove(self.game.getBoard(), False)
            # print(f"Thoi gian: {time.time() - start}")
            self.game.applyMove(computer_move, self.notRedSide)
            print(f"{self.notRedSide.name} choose \033[34m{str(computer_move)}\033[0m")
            self.game.printBoard()
        
        

    def printResult(self):
        print("Result: " + self.game.getStatus())
        control = input("Do you want to continue? (y/n) ")
        if control == "y":
            self.mode[self.control]()
        else:
            exit()

        

def main():
    gameController = GameController()

main()