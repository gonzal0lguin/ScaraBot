# This is a minmax implementation for the game tic tac toe.

import sys
from python_codes.minimax import *

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and not bot.game_over:
            pos = (event.pos[1] // SQ_WIDTH, event.pos[0] // SQ_HEIGHT)

            if bot.player == 2:
                if bot.is_spot_available(pos):
                    bot.update_board(pos)
                    bot.draw_player_fig(pos)
                    if bot.check_win(pos):
                        bot.game_over = True
                        break  # so that the computer doesnt keep playing

                    bot.update_player()

            if bot.player == 1:
                # bot.random_computer_move()
                bot.aiPos = best_move()
                bot.update_board(bot.aiPos)
                bot.draw_player_fig(bot.aiPos)

                if bot.check_win(bot.aiPos):
                    bot.game_over = True

                bot.update_player()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:  # press r key to restart game
                bot.__init__()  # restart the game

    pg.display.update()
