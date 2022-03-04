# This is a minmax implementation for the game tic tac toe.

import sys
from python_codes.minimax import *

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and not game.game_over:
            pos = (event.pos[1] // SQ_WIDTH, event.pos[0] // SQ_HEIGHT)

            if game.player == 2:
                if game.is_spot_available(pos):
                    game.update_board(pos)
                    game.draw_player_fig(pos)
                    if game.check_win(pos):
                        game.game_over = True
                        break  # so that the computer doesnt keep playing

                    game.update_player()

            if game.player == 1:
                # bot.random_computer_move()
                game.aiPos = best_move()
                game.update_board(game.aiPos)
                game.draw_player_fig(game.aiPos)

                if game.check_win(game.aiPos):
                    game.game_over = True

                game.update_player()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:  # press r key to restart game
                game.__init__()  # restart the game

    pg.display.update()
