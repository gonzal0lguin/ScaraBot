#from python_codes.superCatGrid import *
import sys
from python_codes.abPruning_minimax import *
#bot = SuperCat(None)

if bot.mode == 'two players':
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            #print(bot.player)

            if event.type == pg.MOUSEBUTTONDOWN and not bot.game_over:

                origin_cartesian = (event.pos[0], event.pos[1])
                pos_cartesian = bot.original_to_origin((origin_cartesian))
                pos = bot.cartesian_to_polar(pos_cartesian, discrete=True)

                if bot.is_spot_available(pos):
                    bot.update_board(pos, bot.player)
                    bot.draw_player_fig(bot.discrete_polar_to_cartesian(pos))
                    if bot.check_win():
                        bot.game_over = True

                    bot.update_player()

                print(bot.board)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:  # press r key to restart game
                    bot.__init__('two players')  # restart the game

        pg.display.update()

else:
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN and not bot.game_over:

                origin_cartesian = (event.pos[0], event.pos[1])
                pos_cartesian = bot.original_to_origin((origin_cartesian))
                pos = bot.cartesian_to_polar(pos_cartesian, discrete=True)

                if bot.player == 2:
                    if bot.is_spot_available(pos):
                        bot.update_board(pos, bot.player)
                        bot.draw_player_fig(bot.discrete_polar_to_cartesian(pos))
                        if bot.check_win():
                            bot.game_over = True
                            print('human wins')
                            break

                    bot.update_player()


                if bot.player == 1:
                    bot.aiPos = best_move()
                    #bot.random_computer_move()
                    bot.update_board(bot.aiPos, bot.player)
                    print(bot.aiPos)
                    cartesian_pos = bot.discrete_polar_to_cartesian(bot.aiPos)
                    bot.draw_player_fig(cartesian_pos)

                    if bot.check_win():
                        bot.game_over = True

                    bot.update_player()



            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:  # press r key to restart game
                    bot.__init__(None)  # restart the game

        pg.display.update()



