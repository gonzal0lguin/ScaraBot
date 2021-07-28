from python_codes.grid import *

bot = Tac()

scores = {1: 1, 2: -1, 'tie': 0}


def best_move():
    bestPos = (0, 0)
    bestScore = -np.infty

    # check all thte possible spots to take a move
    for i in range(3):
        for j in range(3):
            if bot.is_spot_available((i, j)):
                bot.board[i, j] = 1  # ai player
                score = minimax(bot.board, 0, False)
                bot.board[i, j] = 0  # undo de change

                if score > bestScore:
                    bestScore = score
                    bestPos = (i, j)  # (y, x) dont forget gonzi

    return bestPos


def minimax(board, depth, isMaximizing):
    # base case: terminal state ie.- win / lose / tie (for maximizing player)
    # return 1
    ending = bot.check_end_game()

    if ending != None:  # caso base, se llega al final del juego
        return scores[ending]

    ai = 1
    human = 2

    if isMaximizing:
        maxEval = -np.infty

        for i in range(3):
            for j in range(3):
                if bot.is_spot_available((i, j)):
                    board[i, j] = ai
                    eval = minimax(board, depth + 1, False)
                    board[i, j] = 0
                    maxEval = max(maxEval, eval)
        return maxEval

    else:
        minEval = np.infty
        for i in range(3):
            for j in range(3):
                if bot.is_spot_available((i, j)):
                    board[i, j] = human
                    eval = minimax(board, depth + 1, True)
                    board[i, j] = 0
                    minEval = min(minEval, eval)
        return minEval
