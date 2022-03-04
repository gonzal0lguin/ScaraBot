import numpy as np
import os

#
# ROBOT PARAMETERS
#

grid_centers_mm = np.array([
    [(15.0, 75.0), (-15.0, 75.0), (-45, 75.0)],
    [(15.0, 105.0), (-15.0, 105.0), (-45.0, 105.0)],
    [(15.0, 135.0), (-15.0, 135.0), (-45.0, 135.0)]
])

prueba = [
    [(0, 0), (0, 2)],
    [(1, 0), (1, 2)],
    [(2, 0), (2, 2)],
    [(0, 0), (2, 0)],
    [(0, 1), (2, 1)],
    [(0, 2), (2, 2)],
    [(0, 0), (2, 2)],
    [(0, 2), (2, 0)]
]

#
# GCODE PATHS
#

GRID_PATH = os.getcwd().replace('python_codes', '') + 'gcodes/grid.gcode'
X_PATH =  os.getcwd().replace('python_codes', '') + 'gcodes/X.gcode'
CALIBRATION_PATH = os.getcwd().replace('python_codes', '') + 'gcodes/camera_calibration.gcode'


#
# IMAGE PROCESSING
#

m0 =  "/Users/gonzalolguin/Desktop/tacbot-photos/game/clean.png"
m1 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/calibration.png"
m2 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/grid.png"
m3 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/m1.png"
m4 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/m2.png"
m5 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/m3.png"
m6 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/m4.png"
m7 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/m5.png"
m8 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/m6.png"
m9 = "/Users/gonzalolguin/Desktop/tacbot-photos/game/m7.png"

cali1 = "/Users/gonzalolguin/Desktop/tacbot-photos/cali1.jpg"
cali2 = "/Users/gonzalolguin/Desktop/tacbot-photos/cali2.jpg"

circles = "/Users/gonzalolguin/Desktop/tacbot-photos/game/circlesfull.png"

MAX_RADIUS_px = 15
MIN_RADIUS_py = 5
PIXEL_TO_mm = 0  # factor depends in resolution and distance of camera to object
# to calibrate make a 1mm line in a paper and detect edges
# to count pixels between

ACUMM_RES = 1  # 2 es la mitad de la resulocion de la img original y 3 1/3 ..
CIRCLES_DIST = 120

RESOLUTION = (600, 600)
BOX_L = RESOLUTION[0] // 3
LINE_THICKNESS = 3

N_CORNERS = 4
MIN_QUALTY = 0.3
MIN_CORNER_DIST = 900


CORNERS = [
    [ 240, 1427],
    [ 382,  140],
    [1721, 1311],
    [1601,  134]
  ]