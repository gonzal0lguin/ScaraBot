"""
In pygame coordinates are like:

(0, 0) -> x increase
|
v
y increase

"""

import numpy as np
import pygame as pg


# global constants
HEIGHT = 600
WIDTH = 600
SQ_HEIGHT = HEIGHT // 3
SQ_WIDTH = WIDTH // 3
RADIUS = 60
CROSS_OFFSET = 50
OFFSET = 15

BGcolor = (64, 168, 163)
lineColor = (28, 48, 47)
lineWidth = 10
p1COLOR = (204, 255, 252)
p2COLOR = (145, 145, 145)


class Tac(object):

    def __init__(self, initMove=(0, 0), HEIGHT=HEIGHT, WIDTH=WIDTH, BGFILL=BGcolor):
        # inits the screen, outside the loop

        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.board = np.zeros((3, 3)).astype(int)
        self.player = 1
        self.aiPos = (0, 0)
        self.humanPos = (0, 0)
        self.playerCol = p1COLOR
        self.game_over = False

        self.screen.fill(BGFILL)

        pg.display.set_caption('GATOBOT')
        # draw lines
        # py.draw.line(screen, lineColor, startpos, endpos, width)
        for i in range(1, 3):
            pg.draw.line(self.screen, lineColor, (WIDTH / 3 * i, 0), (WIDTH / 3 * i, HEIGHT), lineWidth)
            pg.draw.line(self.screen, lineColor, (0, HEIGHT / 3 * i), (WIDTH, HEIGHT / 3 * i), lineWidth)

        # self.random_computer_move()
        # self.update_player()

        self.draw_player_fig(initMove)
        self.update_board(initMove)
        self.update_player()

    def is_spot_available(self, pos):
        return self.board[pos] == 0

    def board_full(self):
        for i in range(3):
            for j in range(3):
                if self.is_spot_available((i, j)):
                    return False

        return True

    def update_player(self):
        if self.player == 1:
            self.player = 2
            self.playerCol = p2COLOR
        else:
            self.player = 1
            self.playerCol = p1COLOR

    def update_board(self, pos):
        # pos is a tuple (i, j)
        if self.is_spot_available(pos):
            self.board[pos] = self.player

    def draw_player_fig(self, pos):
        # player 2 is 'o' (human)
        if self.player == 2:
            xpos = int(pos[1] * SQ_WIDTH + SQ_WIDTH / 2)
            ypos = int(pos[0] * SQ_HEIGHT + SQ_HEIGHT / 2)

            pg.draw.circle(self.screen, self.playerCol, (xpos, ypos), RADIUS, lineWidth)

        else:
            x_start = int(pos[1] * SQ_WIDTH + CROSS_OFFSET)
            y_start = int(pos[0] * SQ_HEIGHT + SQ_HEIGHT - CROSS_OFFSET)
            x_end = int(pos[1] * SQ_WIDTH + SQ_WIDTH - CROSS_OFFSET)
            y_end = int(pos[0] * SQ_HEIGHT + CROSS_OFFSET)

            pg.draw.line(self.screen, self.playerCol, (x_start, y_start), (x_end, y_end), lineWidth * 2)
            pg.draw.line(self.screen, self.playerCol, (x_start, y_end), (x_end, y_start), lineWidth * 2)

    def draw_vline(self, pos):
        pg.draw.line(self.screen, self.playerCol, (SQ_WIDTH * pos[1] + SQ_WIDTH / 2, OFFSET),
                     (SQ_WIDTH * pos[1] + SQ_WIDTH / 2, HEIGHT - OFFSET), lineWidth)

    def draw_hline(self, pos):
        pg.draw.line(self.screen, self.playerCol, (OFFSET, SQ_HEIGHT * pos[0] + SQ_HEIGHT / 2),
                     (WIDTH - OFFSET, SQ_HEIGHT * pos[0] + SQ_HEIGHT / 2), lineWidth)

    def draw_asc_line(self):
        pg.draw.line(self.screen, self.playerCol, (OFFSET, OFFSET), (WIDTH - OFFSET, HEIGHT - OFFSET), lineWidth * 2)

    def draw_dec_line(self):
        pg.draw.line(self.screen, self.playerCol, (OFFSET, HEIGHT - OFFSET), (WIDTH - OFFSET, OFFSET), lineWidth * 2)

    def check_win(self, pos):

        for col in range(3):
            if self.board[col, 0] == self.player and self.board[col, 1] == \
                    self.player and self.board[col, 2] == self.player:
                self.draw_hline(pos)
                return True

        for row in range(3):
            if self.board[0, row] == self.player and self.board[1, row] == \
                    self.player and self.board[2, row] == self.player:
                self.draw_vline(pos)
                return True

        if self.board[0, 0] == self.player and self.board[1, 1] == \
                self.player and self.board[2, 2] == self.player:
            self.draw_asc_line()
            return True

        elif self.board[2, 0] == self.player and self.board[1, 1] == \
                self.player and self.board[0, 2] == self.player:
            self.draw_dec_line()
            return True

        return False

    def equal3(self, a, b, c):
        return a == b and b == c and a != 0

    def check_end_game(self):

        for col in range(3):
            if self.equal3(self.board[col, 0], self.board[col, 1], self.board[col, 2]):
                return self.board[col, 0]

        for row in range(3):
            if self.equal3(self.board[0, row], self.board[1, row], self.board[2, row]):
                return self.board[0, row]

        if self.equal3(self.board[0, 0], self.board[1, 1], self.board[2, 2]):
            return self.board[0, 0]

        elif self.equal3(self.board[2, 0], self.board[1, 1], self.board[0, 2]):
            return self.board[1, 1]

        elif self.board_full():
            return 'tie'

        return None

    def random_computer_move(self):
        rand_pos = (np.random.randint(0, 3), np.random.randint(0, 3))

        if self.is_spot_available(rand_pos):
            self.aiPos = rand_pos
            self.update_board(rand_pos)
            self.draw_player_fig(rand_pos)
            # print(rand_pos)

        else:
            self.random_computer_move()

    def get_winner_coords(self):
        "return x_start, y_start and x_end, y_end"
        pass