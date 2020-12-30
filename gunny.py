import numpy as np
import random
import time


class State:
    def __init__(self, board, score):
        self.board = board.copy()
        self.score = score

def bestMove():
    global current_player, board, points, global_depth
    global_depth += 1
    best_score = np.Infinity
    move = (-1, -1)
    for ngang in range(2):
            for choose in range(n):
                board2 = np.copy(board)
                if ngang == 1:
                    if (board2[choose, :].any() != 0):
                        board2[choose,:] = np.full(n,0)
                        score = minimax(board2,global_depth +1, True)
                        if score < best_score:
                            best_score = score
                            move = (ngang, choose)
                else:
                    if (board2[:, choose].any() != 0):
                        board2[:, choose] = np.full(n,0)
                        score = minimax(board2, global_depth+1, True)
                        if score < best_score:
                            best_score = score
                            move = (ngang, choose)

    ngang, choose = move

    if ngang == 1:
        points += np.sum(board[choose,:])
        board[choose,:] = np.full(n,0)
    else:
        points += np.sum(board[:,choose])
        board[:,choose] = np.full(n,0)

    print("AI move: ", move)
    print(board)
    print(f"\n Depth: {global_depth} HUMAN: {points} \n")
    
    current_player = 1

def minimax(board, depth, isMaximizing):
    global MAX_BUOC
    if depth == MAX_BUOC +1:
        return - np.sum(board)

    if isMaximizing:
        best_score = -np.Infinity
        for ngang in range(2):
            for choose in range(n):
                board2 = np.copy(board)
                if ngang == 1:
                    if (np.any(board2[choose, :] != 0)):
                        board2[choose,:] = np.full(n,0)
                        score = minimax(board2, depth+1, False)
                        best_score = max(score, best_score)
                else:
                    if (np.any(board2[:,choose] != 0)):
                        board2[:, choose] = np.full(n,0)
                        score = minimax(board2, depth+1, False)
                        best_score = max(score, best_score)

        return best_score


    else:
        best_score = np.Infinity
        for ngang in range(2):
            for choose in range(n):
                if depth == 2:
                    tt = 1
                board2 = np.copy(board)
                if ngang == 1:
                    if (np.any(board2[choose, :] != 0)):
                        board2[choose,:] = np.full(n,0)
                        score = minimax(board2, depth+1, True)
                        best_score = min(score, best_score)
                else:
                    if (np.any(board2[:,choose] != 0)):
                        board2[:, choose] = np.full(n,0)
                        if depth == 2 and choose == 3:
                            tttt = 1
                        score = minimax(board2, depth+1, True)
                        best_score = min(score, best_score)
        return best_score


n = 10
points = 0
# board = np.array([
#     [-1, 7, -2, 5],
#     [+2, -6, +3, -5],
#     [-4, +9, -3, +4],
#     [+1, -7, +7, -10]]
# )
# DULIEUMAU = [[1,-6,7,-7,8,18],
#             [-8,2,-4,-9,16,9],
#             [14,-11,3,-10,-5,13],
#             [10,17,-12,4,-1,-13],
#             [-15,15,-2,-3,5,-14],
#             [11,-16,12,-17,-18,6]]
# board = np.array(DULIEUMAU)
board = np.full((n,n),0)
for i in range(n):
    for j in range(n):
        board[i,j] = np.random.randint(-9,9)

sumb = np.sum(board)
board[0,0] = board[0,0] - sumb
print("sum", np.sum(board))
current_player = 1
# board = (-1) * board
MAX_BUOC = 8
global_depth = 0
# bestMove()
print(board)



while global_depth < MAX_BUOC and board.any() != 0:
    if current_player == 1:
        du_lieu_vao = input("Nhap: ")
        if du_lieu_vao[0] == 'h':
            ngang = 1
        else:
            ngang = 0
        choose = int(du_lieu_vao[1])
        # ngang, choose = [int(i) for i in input().split()]
        if ngang == 1:
            points += np.sum(board[choose,:])
            board[choose,:] = np.full(n,0)
        else:
            points += np.sum(board[:,choose])
            board[:,choose] = np.full(n,0)
        global_depth += 1
        print(board)
        print(f"\n Depth: {global_depth}  HUMAN: {points} \n")

    if global_depth >= MAX_BUOC:
        break
    else:
        start = time.time()
        bestMove()
        print(f"Thoi gian: {time.time() - start}")

print()




# du_lieu_step2 = np.copy(DULIEUMAU)
# du_lieu_step2[:,5] = np.full(n,0)
# du_lieu_step2[:,0] = np.full(n,0)
# du_lieu_step2[:,3] = np.full(n,0)
# # du_lieu_step2[0,:] = np.full(n,0)
# print(du_lieu_step2)
# print(minimax(du_lieu_step2,2,False))
# print(du_lieu_step2)