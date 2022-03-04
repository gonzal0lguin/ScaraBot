//
// Created by Gonzalo Olguin on 02-02-22.
//

#ifndef SUPERCATCPP_CATBOT_H
#define SUPERCATCPP_CATBOT_H

#include <SFML/Graphics.hpp>
#include <cmath>
#include <iostream>

using namespace sf;
using namespace std;

typedef unsigned int uint;

#define WIDTH 1400
#define HEIGHT 1400
#define CIRCLE_RADIUS 30
#define CROSS_LENGTH 60
#define CELL_HEIGHT 150
#define CELL_WIDTH 45

#define P0_WINCODE 0
#define P1_WINCODE 1
#define TIE_CODE 2
#define NOWIN_CODE 3

#define ROWS 8
#define COLS 4

class CatBot {
public:
    // VARIABLES
    RenderWindow window;

    CircleShape s1, s2, s3, s4;
    RectangleShape l1, l2, l3, l4;
    CircleShape grid_circles[4] = {s1, s2, s3, s4};
    RectangleShape grid_lines[4] = {l1, l2, l3, l4};

    vector<CircleShape> circles;
    vector<RectangleShape>exes;

    //FUNCTIONS
    CatBot(); // init

    static int *cartesian_to_discrete_polar(Vector2i localPosition);
    static int *polar_to_grid_cartesian(int r, int theta);
    int update_bits(int player, int row_ind, int bit_pos);
    void undo_move(int player, int row_ind, int bit_pos);
    void draw_figures();
    int check_win();
    int check_full_board();
    void draw_grid();
    void update_figures(int r, int theta, bool &player);

//private:

    // rows - cols bit maps for each player
    bool _player = true;
    uint lp0_r0 = 0b00000000;
    uint lp0_r1 = 0b00000000;
    uint lp0_r2 = 0b00000000;
    uint lp0_r3 = 0b00000000;

    uint lp1_r0 = 0b00000000;
    uint lp1_r1 = 0b00000000;
    uint lp1_r2 = 0b00000000;
    uint lp1_r3 = 0b00000000;

    uint bit_matrix[2][4] = { {lp0_r0, lp0_r1, lp0_r2, lp0_r3},
                              {lp1_r0, lp1_r1, lp1_r2, lp1_r3} };

    uint MASK_C1 = 0b10000111;
    uint MASK_C2 = 0b11000011;
    uint MASK_C3 = 0b11100001;

    uint SPIRAL_CCWC1 = 1;
    uint SPIRAL_CCWC2 = 1<<7;
    uint FULL_BOARD = 0x3FC;
    uint ROW4MASK = 0xF;

    uint SPECIALCASES[6][4] = {{0b00100000, 0b01000000, 0b10000000, 0b00000001},
                               {0b01000000, 0b10000000, 0b00000001, 0b00000010},
                               {0b10000000, 0b00000001, 0b00000010, 0b00000100},
                               {0b00000001, 0b10000000, 0b01000000, 0b00100000},
                               {0b00000010, 0b00000001, 0b10000000, 0b01000000},
                               {0b00000100, 0b00000010, 0b00000001, 0b10000000}};
};

#endif

/*
0b00000001;
0b00100000;
0b01000000;
0b10000000;

0b00000001;
0b00000010;
0b01000000;
0b10000000;

0b00000001;
0b00000010;
0b00000100;
0b10000000;

*/