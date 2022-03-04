# grid for the game "super cat"

import numpy as np
import pygame as pg

HEIGHT = 800
WIDTH = 800
SQ_HEIGHT = HEIGHT // 3
SQ_WIDTH = WIDTH // 3
RADIUS = 60
CROSS_OFFSET = 50
OFFSET = 15

BGcolor = (64, 168, 163)
lineColor = (28, 48, 47)
lineWidth = 7
p1COLOR = (204, 255, 252)
p2COLOR = (145, 145, 145)

ROWS = 4
COLUMNS = 8


class SuperCat(object):

    def __init__(self, mode=None, WIDTH=WIDTH, HEIGHT=HEIGHT):

        pg.init()
        self.mode = mode
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.board = np.zeros((4, 8)).astype(int)
        self.player = 1
        self.aiPos = (0, 0)
        self.humanPos = (0, 0)
        self.playerCol = p1COLOR
        self.game_over = False

        self.screen.fill(BGcolor)

        pg.display.set_caption('GATOBOT')

        self.draw_grid()
        self.random_computer_move()
        self.update_player()

    def draw_grid(self):
        xm = int(WIDTH / 2 * (1 - 1 / np.sqrt(2)))
        ym = xm
        xp = int(WIDTH / 2 * (1 + 1 / np.sqrt(2)))
        yp = xp

        for i in range(1, 5):
            pg.draw.circle(self.screen, lineColor, (WIDTH // 2, HEIGHT // 2), 100 * i, lineWidth)

        pg.draw.line(self.screen, lineColor, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), lineWidth)
        pg.draw.line(self.screen, lineColor, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), lineWidth)
        pg.draw.line(self.screen, lineColor, (xm, ym), (xp, yp), lineWidth)
        pg.draw.line(self.screen, lineColor, (xm, yp), (xp, ym), lineWidth)

    def is_spot_available(self, pos):
        if pos[0] <= 3 and pos[1] <= 7:
            return self.board[pos] == 0

    def original_to_origin(self, pos, displacement=(WIDTH / 2, WIDTH / 2)):
        return (pos[0] - displacement[0], -pos[1] + displacement[1])

    def origin_to_original(self, pos, displacement=(WIDTH / 2, WIDTH / 2)):
        return (pos[0] + displacement[0], (-pos[1] + displacement[1]))

    def cartesian_to_polar(self, coord, discrete=False):
        r = np.sqrt(coord[0] ** 2 + coord[1] ** 2)
        theta = np.arctan2(coord[1], coord[0])

        if discrete:
            r = int(r // (WIDTH // 8))
            theta = int((theta * 180 / np.pi))

        return (r, theta // 45)

    def discrete_polar_to_cartesian(self, polarPos, OFFSET_r=50, OFFSET_t=22.5):
        rd = 100 * polarPos[0] + OFFSET_r
        thetad = (45 * polarPos[1] + OFFSET_t) * np.pi / 180

        x = rd * np.cos(thetad)
        y = rd * np.sin(thetad)

        return self.origin_to_original((x, y))

    def board_full(self):
        return (self.board != 0).all()

    def update_board(self, pos, player):
        if pos[0] <= 3 and pos[1] <= 7:
            self.board[pos[0], pos[1]] = player

    def update_player(self):
        if self.player == 1:
            self.player = 2
            self.playerCol = p2COLOR
        else:
            self.player = 1
            self.playerCol = p1COLOR

        #print(self.player)

    def draw_x_from_center_point(self, center, l, color, lineWidth):
        x0, y0 = center
        x, y = l/2/np.sqrt(2), l/2/np.sqrt(2)
        start_1 = (x0-x, y0-y)
        end_1 = (x0+x, y0+y)
        start_2 = (x0-x, y0+y)
        end_2 = (x0+x, y0-y)

        pg.draw.line(self.screen, color, start_1, end_1, lineWidth)
        pg.draw.line(self.screen, color, start_2, end_2, lineWidth)

    def draw_player_fig(self, pos):

        if np.sqrt((-WIDTH/2+pos[0])**2 + (WIDTH/2-pos[1])**2) < 100:

            if self.player == 2:
                pg.draw.circle(self.screen, self.playerCol, pos, 15, lineWidth)

            else:
                self.draw_x_from_center_point(pos, 25, self.playerCol, lineWidth)

        else:
            if self.player == 2:
                pg.draw.circle(self.screen, self.playerCol, pos, 30, lineWidth)

            else:
                self.draw_x_from_center_point(pos, 55, self.playerCol, lineWidth+3)

    def draw_win_line(self, pos, color):
        start = (WIDTH/2, HEIGHT/2)
        end = self.discrete_polar_to_cartesian(pos)
        pg.draw.line(self.screen, color, start, end, lineWidth)

    def draw_arc_line(self):
        rect = [0, WIDTH, HEIGHT, 300]
        pg.draw.arc(self.screen, self.playerCol, rect, 0, np.pi/2, lineWidth)

    def check_end_game(self):
        # line
        for j in range(COLUMNS):
            if (self.board[:, j] == 1).all() or (self.board[:, j] == 2).all():
                #self.draw_win_line(pos, self.playerCol)
                return self.board[0, j]

        #arc
        for i in range(ROWS):
            for j in range(8):
                if self.board[i, 2-j] == self.board[i, 1-j] == self.board[i, -j] == self.board[i, -(1+j)] \
                    and self.board[i, 2-j] != 0:
                    return self.board[i, 2-j]

        for i in range(ROWS):
            for j in range(8):
                if self.board[2-i, 2-j] == self.board[1-i, 1-j] == self.board[-i, -j] == self.board[-1-i, -(1+j)] \
                    and self.board[2-i, 2-j] != 0:
                    return self.board[2-i, 2-j]

        for i in range(ROWS):
            for j in range(8):
                if self.board[0, 2-j] == self.board[1, 1-j] == self.board[2, -j] == self.board[3, -(1+j)] \
                    and self.board[0, 2-j] != 0:
                    return self.board[0, 2-j]

        if self.board_full():
            return 'tie'



    def check_win(self):
        # line
        for j in range(COLUMNS):
            if (self.board[:, j] == 1).all() or (self.board[:, j] == 2).all():
                #self.draw_win_line(pos, self.playerCol)
                return True

        #arc
        for i in range(ROWS):
            for j in range(8):
                if self.board[i, 2-j] == self.board[i, 1-j] == self.board[i, -j] == self.board[i, -(1+j)] \
                    and self.board[i, 2-j] != 0:
                    return True

        for i in range(ROWS):
            for j in range(8):
                if self.board[2-i, 2-j] == self.board[1-i, 1-j] == self.board[-i, -j] == self.board[-1-i, -(1+j)] \
                    and self.board[2-i, 2-j] != 0:
                    return True

        for i in range(ROWS):
            for j in range(8):
                if self.board[0, 2-j] == self.board[1, 1-j] == self.board[2, -j] == self.board[3, -(1+j)] \
                    and self.board[0, 2-j] != 0:
                    return True

        return None


    def random_computer_move(self):
        rand_pos = (np.random.randint(0, 4), np.random.randint(0, 8))

        if self.is_spot_available(rand_pos):
            self.aiPos = rand_pos
            self.update_board(rand_pos, self.player)
            self.draw_player_fig(self.discrete_polar_to_cartesian(rand_pos))
            #print(rand_pos)

        else:
            self.random_computer_move()



class TranspositionTable(object):

    def __init__(self):
        self.zobrist_table = np.zeros(2*4*8, dtype=np.int64)
        self.init_table()

    def init_table(self):
        i64 = np.iinfo(np.int64)
        for k in range(2*4*8):
                    self.zobrist_table[k] = np.random.randint(i64.min, i64.max, dtype=np.int64)
