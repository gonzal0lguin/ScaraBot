from python_codes.Robot_driver import Scara
from python_codes.Camera import Camera
from python_codes.SerialDevice import SerialDevice
from python_codes.minimax import *
from python_codes.defaults import *
import time

cam = Camera()
serial_dev = SerialDevice()
bot = Scara(serial_dev)

time.sleep(2) # wait to initialize

bot.home()

_ = input("press enter to calibrate robot")

while True:
    ok = cam.capture(calibration=True)
    if not ok:
        moveon = input('Robot not calibrated properly... Redraw calibration? [y/n]')
        if moveon == 'n': break
        else: pass

_ = input("Robot OK... Press enter to start game")

bot.draw_grid()

t_last = time.time()
last_len = len(cam.user_moves)

while(not game.game_over):

        while( game.player == 2):
            if (time.time() - t_last > 1):
                cam.capture()
                cam.get_user_coords()
                if (last_len != len(cam.user_moves)):
                    print('new human move in: ', cam.last_user_move)
                    pos = cam.last_user_move
                    if game.is_spot_available(pos):
                        game.update_board(pos)

                        if game.check_win(pos):
                            game.game_over = True
                            break  # so that the computer doesnt keep playing

                        game.update_player()
                        last_len = len(cam.user_moves)

                t_last_check = time.time()

        if game.player == 1:
            # bot.random_computer_move()
            game.aiPos = best_move()
            game.update_board(game.aiPos)
            bot.draw_fig(game.aiPos)

            end = game.check_end_game()
            if end[0] == 1:
                bot.draw_win_line(end[1])
                print('You Loose!')
                game.game_over = True

            game.update_player()