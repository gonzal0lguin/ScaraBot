# This is a minmax implementation for the game tic tac toe.
import sys
from python_codes.grid import *

bot = Tac()

while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()

        if event.type == py.MOUSEBUTTONDOWN and not bot.game_over:
            pos = (event.pos[1] // SQ_WIDTH, event.pos[0] // SQ_HEIGHT)

            if bot.player == 2:
                if bot.is_spot_available(pos):
                    bot.update_board(pos)
                    bot.draw_player_fig(pos)
                    if bot.check_win(pos):
                        bot.game_over = True
                        break # para que no siga jugando el bot

                    bot.update_player()

            if bot.player == 1:
                bot.random_computer_move()
                if bot.check_win(bot.aiPos):
                    bot.game_over = True

                bot.update_player()

            #bot.update_player()

        if event.type == py.KEYDOWN:
            if event.key == py.K_r:
                bot.__init__()  # restart the game

    py.display.update()
