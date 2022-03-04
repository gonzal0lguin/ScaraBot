import numpy as np

class Tac(object):

    def __init__(self, botFirst=True, initMove=(0, 0)):
        # inits the screen, outside the loop

        self.board = np.zeros((3, 3)).astype(int)
        self.player = 1 if botFirst else 2
        self.aiPos = (0, 0)
        self.humanPos = (0, 0)
        self.game_over = False

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
        else:
            self.player = 1

    def update_board(self, pos):
        # pos is a tuple (i, j)
        if self.is_spot_available(pos):
            self.board[pos] = self.player

    def check_win(self):

        for col in range(3):
            if self.board[col, 0] == self.player and self.board[col, 1] == \
                    self.player and self.board[col, 2] == self.player:
                return True

        for row in range(3):
            if self.board[0, row] == self.player and self.board[1, row] == \
                    self.player and self.board[2, row] == self.player:
                return True

        if self.board[0, 0] == self.player and self.board[1, 1] == \
                self.player and self.board[2, 2] == self.player:
            return True

        elif self.board[2, 0] == self.player and self.board[1, 1] == \
                self.player and self.board[0, 2] == self.player:
            return True

        return False

    def equal3(self, a, b, c):
        return a == b and b == c and a != 0

    def check_end_game(self):

        for col in range(3):
            if self.equal3(self.board[col, 0], self.board[col, 1], self.board[col, 2]):
                win_cords = [(col, 0), (col, 2)]
                return [self.board[col, 0], win_cords]

        for row in range(3):
            if self.equal3(self.board[0, row], self.board[1, row], self.board[2, row]):
                win_cords = [(0, row), (2, row)]
                return [self.board[0, row], win_cords]

        if self.equal3(self.board[0, 0], self.board[1, 1], self.board[2, 2]):
            win_cords = [(0, 0), (2, 2)]
            return [self.board[0, 0], win_cords]

        elif self.equal3(self.board[2, 0], self.board[1, 1], self.board[0, 2]):
            win_cords = [(2, 0), (0, 2)]
            return [self.board[1, 1], win_cords]

        elif self.board_full():
            # TODO: return places where there are x, so it draws 3 even in a tie
            return ['tie', 0]

        return None

    def random_computer_move(self):
        rand_pos = (np.random.randint(0, 3), np.random.randint(0, 3))

        if self.is_spot_available(rand_pos):
            self.aiPos = rand_pos
            self.update_board(rand_pos)
            # print(rand_pos)

        else:
            self.random_computer_move()

    def get_winner_coords(self):
        "return x_start, y_start and x_end, y_end"
        pass
