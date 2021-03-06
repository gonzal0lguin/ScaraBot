#from python_codes.grid import *
from python_codes.superCatGrid import *
bot = SuperCat('two playes')

scores = {1: 1, 2: -1, 'tie': 0}
ROWS = 3
COLUMNS = 3

def best_move():
    bestPos = (0, 0)
    bestScore = -np.infty

    # check all thte possible spots to take a move
    for i in range(ROWS):
        for j in range(COLUMNS):
            if bot.is_spot_available((i, j)):
                bot.board[i, j] = 1  # ai player
                score = minimax(bot.board, 0, False)
                bot.board[i, j] = 0  # undo de change

                if score > bestScore:
                    bestScore = score
                    bestPos = (i, j)  # (y, x) dont forget gonzi

    return bestPos


def minimax(board, depth, isMaximizing, alpha=-np.infty, beta=np.infty):
    # base case: terminal state ie.- win / lose / tie (for maximizing player)
    # return 1
    ending = bot.check_end_game()
    print(isMaximizing)
    if ending != None:  # caso base, se llega al final del juego
        return scores[ending]

    ai = 1
    human = 2

    if isMaximizing:
        maxEval = -np.infty
        for i in range(ROWS):
            for j in range(COLUMNS):
                if bot.is_spot_available((i, j)):
                    board[i, j] = ai
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i, j] = 0
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, maxEval)
                    if beta <= alpha:
                        break

        return maxEval

    else:
        minEval = np.infty
        for i in range(ROWS):
            for j in range(COLUMNS):
                if bot.is_spot_available((i, j)):
                    board[i, j] = human
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i, j] = 0
                    minEval = min(minEval, eval)
                    beta = min(minEval, beta)
                    if beta <= alpha:
                        break
        return minEval
