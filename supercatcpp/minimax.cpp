//
// Created by Gonzalo Olguin on 12-02-22.
//

//
// Created by Gonzalo Olguin on 20-01-22.
//

#include "minimax.h"
#include "CatBot.h"

#include <iostream>
#include <climits>
#include <thread>

using namespace std;

CatBot bot;

int scores[3] = {1, -1, 0};

int minimax(int depth, int isMaximizing, int alpha, int beta) {

    int end = bot.check_win();
    if (end != 3 || depth == 0) { // game over (base case)
        return scores[end];
    }

    int ai_ind = 0;
    int human_ind = 1;

    if (isMaximizing) {
        int maxEval = INT_MIN;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 8; j++) {
                if (bot.update_bits(ai_ind, i, j)) {
                    int eval = minimax(depth - 1, false, alpha, beta);
                    bot.undo_move(ai_ind, i, j);
                    maxEval = max(maxEval, eval);
                    alpha = max(alpha, maxEval);
                    if (alpha >= beta)
                        break;
                }
            }
        }
        return maxEval;
    }

    else {
        int minEval = INT_MAX;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 8; j++) {
                if (bot.update_bits(human_ind, i, j)) {
                    int eval = minimax(depth - 1, true, alpha, beta);
                    bot.undo_move(human_ind, i, j);
                    minEval = min(minEval, eval);
                    beta = min(minEval, beta);
                    if (alpha >= beta)
                        break;
                }
            }
        }
        return minEval;
    }
}

int *bestMove() {
    static int bestPos[2] = {0, 0};
    int bestScore = INT_MIN;

    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 8; j++) {
            if (bot.update_bits(0, i, j)) { // we use player 0 as AI
                int score = minimax(6, false);
                bot.undo_move(0, i, j);

                if (score > bestScore) {
                    bestScore = score;
                    bestPos[0] = i;
                    bestPos[1] = j;
                }
            }
        }
    }
    return bestPos;
}


int *threaded_bestMove() {
    static int bestPos[2] = {0, 0};
    int bestScore = INT_MIN;
    vector<thread> _threads;
    vector<int> thread_score(ROWS * COLS);
    vector<int*> pos;
    // TODO: use 1 thread for each position -> 32 threads
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 8; j++) {
            if (bot.update_bits(0, i, j)) { // we use player 0 as AI
                //int score = minimax(6, false);
                _threads.(minimax, DEPTH, false);
                bot.undo_move(0, i, j);
                int score=0;
                if (score > bestScore) {
                    bestScore = score;
                    bestPos[0] = i;
                    bestPos[1] = j;
                }
            }
        }
    }
    for (auto &t : _threads){
        if (t.joinable())
            t.join();
    }

    // TODO: calculate best position related to highest score
    return bestPos;
}


