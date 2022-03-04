//
// Created by Gonzalo Olguin on 02-02-22.
//

#include "CatBot.h"

CatBot::CatBot() {
    window.create(VideoMode(WIDTH, HEIGHT), "SuperCat game");

    for (int i=3; i>= 0; i--) {
        grid_circles[i].setRadius(CELL_HEIGHT + (float) i * CELL_HEIGHT);
        grid_circles[i].setOrigin(CELL_HEIGHT + (float) i * CELL_HEIGHT, CELL_HEIGHT + (float) i * CELL_HEIGHT);
        grid_circles[i].setPosition(WIDTH/2.f, HEIGHT/2.f);
        grid_circles[i].setFillColor(Color::Transparent);
        grid_circles[i].setOutlineColor(Color::White);
        grid_circles[i].setOutlineThickness(10);

        grid_lines[i].setSize(Vector2f(1200, 10));
        grid_lines[i].setOrigin(600,5);
        grid_lines[i].setPosition(WIDTH/2.f,HEIGHT/2.f);
        grid_lines[i].rotate((float )i*45);
    }

    cout << "bot initialized\n";
}

int *CatBot::cartesian_to_discrete_polar(Vector2i localPosition) {
    static int pos[2];
    float x = (float) localPosition.x - WIDTH / 2.f;
    float y = -(float) localPosition.y + HEIGHT / 2.f;
    float theta = atan2f(y, x) * 180 / M_PI;
    if (theta < 0)
        theta += 360;
    theta /= 45;
    int r = (int) sqrt(x * x + y * y) / 150;

    pos[0] = r;
    pos[1] = (int) theta;
    return pos;
}

int *CatBot::polar_to_grid_cartesian(int r, int theta) {
    static int pos[2];
    //cout << "r= " << CELL_HEIGHT * r + CELL_HEIGHT / 2.f << "  theta= " << (theta + .5) * CELL_WIDTH << endl;
    int x = (CELL_HEIGHT * r + CELL_HEIGHT / 2) * cos((theta + .5) * CELL_WIDTH * M_PI / 180);
    int y = (CELL_HEIGHT * r + CELL_HEIGHT / 2) * sin((theta + .5) * CELL_WIDTH * M_PI / 180);
    pos[0] = x;
    pos[1] = y;
    return pos;
}

int CatBot::update_bits(int player, int row_ind, int bit_pos) {
    /*
     * Updates bit matrix for a given player in a given position
     * if it is possible. Returns 1 if possible and 0 otherwise.
     */

    uint mask = 1 << bit_pos;
    // check if position is available
    if (!(bit_matrix[player][row_ind] & mask) &&
        !(bit_matrix[!player][row_ind] & mask)) {
        bit_matrix[player][row_ind] += mask;
        return 1;
    }

    return 0;
}

void CatBot::undo_move(int player, int row_ind, int bit_pos) {
    uint mask = 1 << bit_pos;
    bit_matrix[player][row_ind] -= mask;
}

int CatBot::check_win() {

    /*
     *  win in a vertical line
     */
    if ((bit_matrix[0][0] & bit_matrix[0][1] &
         bit_matrix[0][2] & bit_matrix[0][3]) != 0) {
        return P0_WINCODE; // player 0
    } else if ((bit_matrix[1][0] & bit_matrix[1][1] &
                bit_matrix[1][2] & bit_matrix[1][3]) != 0) {
        return P1_WINCODE; // player 1
    }

    /*
     * check for semi-circle
     */

    // center cases
    for (int i = 0; i < 4; i++) {
        uint mask = 0b1111;
        for (int j = 0; j < 5; j++) {
            if ((bit_matrix[0][i] & mask) == mask) {
                return P0_WINCODE; // player 0 wins
            } else if ((bit_matrix[1][i] & mask) == mask) {
                return P1_WINCODE; // player 1 wins
            }
            mask <<= 1;
        }

        if ((bit_matrix[0][i] & MASK_C1) == MASK_C1 ||
            (bit_matrix[0][i] & MASK_C2) == MASK_C2 ||
            (bit_matrix[0][i] & MASK_C3) == MASK_C3) {
            return P0_WINCODE; // player 0 wins in a special case
        }
        else if ((bit_matrix[1][i] & MASK_C1) == MASK_C1 ||
                   (bit_matrix[1][i] & MASK_C2) == MASK_C2 ||
                   (bit_matrix[1][i] & MASK_C3) == MASK_C3) {
            return P1_WINCODE; // player 0 wins in a special case
        }
    }

    // spiral win (the most painful to program)
    // clockwise
    uint mask= 1;
    for (int i= 0; i< 5; i++) {
        uint sum_p0 = ((mask << i) & bit_matrix[0][0]) +
                      ((mask << (i + 1)) & bit_matrix[0][1]) +
                      ((mask << (i + 2)) & bit_matrix[0][2]) +
                      ((mask << (i + 3)) & bit_matrix[0][3]);

        if (sum_p0 == (ROW4MASK << i)) {
            return P0_WINCODE;
        } else if (((mask << i) & bit_matrix[1][0] +
                    (mask << (i + 1)) & bit_matrix[1][1] +
                    (mask << (i + 2)) & bit_matrix[1][2] +
                    (mask << (i + 3)) & bit_matrix[1][3]) ==
                   (ROW4MASK << i)) {
            return P1_WINCODE;
        }
    }

    //pal otro lao
    for (int i= 7; i>= 3; i--) {
        uint sum_p0 = ((mask << i) & bit_matrix[0][0]) +
                      ((mask << (i - 1)) & bit_matrix[0][1]) +
                      ((mask << (i - 2)) & bit_matrix[0][2]) +
                      ((mask << (i - 3)) & bit_matrix[0][3]);

        if (sum_p0 == (ROW4MASK << i)) {
            return P0_WINCODE;
        } else if (((mask << i) & bit_matrix[1][0] +
                    (mask << (i - 1)) & bit_matrix[1][1] +
                    (mask << (i - 2)) & bit_matrix[1][2] +
                    (mask << (i - 3)) & bit_matrix[1][3]) ==
                   (ROW4MASK << i)) {
            return P1_WINCODE;
        }
    }
    // special cases
    int p0= 0, p1= 0;
    for (auto & i : SPECIALCASES){
        for (int j= 0; j< 4; j++){
            if ( (bit_matrix[0][j] & i[j]) != 0) {
                p0++;
            }
            else if ((bit_matrix[1][j] & i[j]) != 0) {
                p1++;
            }
            else {
                continue;
            }
        }
        if (p1==4) return P1_WINCODE;
        else if (p0==4) return P0_WINCODE;
        else{
            p1=0;
            p0=0;
        }
    }

    // tie (practically impossible to reach btw)
    if (check_full_board())
        return TIE_CODE; // index of a tie

    return NOWIN_CODE; // index of game not finished
}

int CatBot::check_full_board() {
    uint sum = 0;
    for (int i = 0; i < 4; i++) {
        sum += bit_matrix[0][i] + bit_matrix[1][i];
    }

    if (sum == FULL_BOARD)
        return 1;

    return 0;
}

void CatBot::update_figures(int r, int theta, bool &player) {
    int *pos = polar_to_grid_cartesian(r, theta);

    if (player){ // x player

        RectangleShape l1, l2;
        l1.setSize(Vector2f(CROSS_LENGTH, 10));
        l1.setOrigin(CROSS_LENGTH / 2, 5);
        l1.setPosition(pos[0] + 700.f, 700.f - pos[1]);
        l1.rotate((float )45);

        l2.setSize(Vector2f(CROSS_LENGTH, 10));
        l2.setOrigin(CROSS_LENGTH / 2, 5);
        l2.setPosition(pos[0] + 700.f, 700.f - pos[1]);
        l2.rotate(-(float )45);

        exes.push_back(l1);
        exes.push_back(l2);
    }

    else{ // circles

        CircleShape circle;
        if (r > 0) {
            circle.setRadius(CIRCLE_RADIUS);
        }
        else{
            circle.setRadius(CIRCLE_RADIUS/2);
        }
        circle.setOrigin(CIRCLE_RADIUS / 2.f, CIRCLE_RADIUS / 2.f);
        circle.setFillColor(Color::Black);
        circle.setOutlineThickness(10);
        circle.setOutlineColor(Color::White);
        circle.setPosition((float )pos[0] + 700.f, -(float )pos[1] + 700.f);

        circles.push_back(circle);
    }

    player = !player;
}

void CatBot::draw_figures() {
    for (auto & circle : circles)
        window.draw(circle);

    for (auto & ex : exes)
        window.draw(ex);
}

void CatBot::draw_grid() {
    for (const auto & circle : grid_circles)
        window.draw(circle);

    for (const auto & line : grid_lines)
        window.draw(line);
}


