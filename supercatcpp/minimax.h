//
// Created by Gonzalo Olguin on 12-02-22.
//

#ifndef SUPERCATCPP_MINIMAX_H
#define SUPERCATCPP_MINIMAX_H

#include <climits>

const int DEPTH = 6;

int *bestMove();
int minimax(int depth, int isMaximizing, int alpha=INT_MIN, int beta=INT_MAX);
int *threaded_bestMove();

#endif //SUPERCATCPP_MINIMAX_H
