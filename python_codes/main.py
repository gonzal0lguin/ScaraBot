from time import sleep
import cv2 as cv
import numpy as np
import time
from python_codes.Camera import Camera
from python_codes.defaults import *

SIM_REFRESH_RATE = 3
CHECK_RATE = 1
imgs = [m0, m1, m2, m3, m4, m5, m6, m7, m8, m9]
newMove = False

imgs_index = 0
t_last_sim = time.time()
t_last_check = time.time()


time.sleep(1)

cam = Camera(True)
cam.capture(cv.imread(m1)[200:-1, 400:2400], True) # calibration

last_len = len(cam.user_moves)
img = cv.imread(imgs[imgs_index])

while (imgs_index != len(imgs)):

    # cv.imshow('processed', cam.curr)
    # cv.imshow('original', img)


    if (time.time() - t_last_sim) > SIM_REFRESH_RATE:
        t_last_sim = time.time()
        imgs_index += 1

    if (time.time() - t_last_check) > CHECK_RATE:
        img = cv.imread(imgs[imgs_index])[200:-1, 400:2400]
        cam.capture(img)
        cam.get_user_coords()
        if (last_len != len(cam.user_moves)):
            cam.draw_grid()
            print('new move in: ', cam.last_user_move)
            last_len = len(cam.user_moves)
        t_last_check = time.time()

    cv.imshow('cal', cam.calibration_img)
    cv.imshow('img', img)
    cv.imshow('processed', cam.curr)
    cv.waitKey(1)

# TODO:
#  bot.init() & bot.draw_calibration()
#  cam.capture(calibration)
#       while(true):
#           if turn == bot:
#               gridPos = best_move()
#               catBot.update(gridPos)
#               real_pos_mm = bot.grid_to_real_position(gridPos)
#               bot.draw_X(real_pos_mm)
#               turn = human
#           else:
#               if (time.time() - t_last_check) > CHECK_RATE:
#                   cam.capture()
#                   cam.get_user_coords()
#                   if (last_len != len(cam.user_moves)): // or cam.last_user_move not in algo lol
#                       catBot.update(cam.lastMove)
#                       last_len = len(cam.user_moves)
#                       turn = bot
#                   t_last_check = time.time()
#
