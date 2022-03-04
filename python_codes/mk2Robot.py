import numpy as np
import matplotlib.pyplot as plt
from python_codes.transformations import *
from time import time_ns

class MK2Robot(object):
    HOME_0 = 0
    HOME_1 = np.pi

    def __init__(self, link_lengths):
        self.a = link_lengths
        self.q = []
        self.T = []
        self.pose = []
        self.s = []
        self.home = (0, 90)  # deg
        self.home_cartesian = (link_lengths[0], link_lengths[1])

        # self.update_pose(MK2Robot.HOME_0, MK2Robot.HOME_1)

    def update_pose(self, q0, q1):
        """
        Este metodo calcula la pose de cada link del robot, usando las matrices T y R. Luego guarda el
        resultado para cada link como un elemento del arreglo self.pose
        """
        # Calcula las matrices T y Q
        self._update_transformation_matrices(q0, q1)

        # re-escribe self.pose como una lista de 4 matrices nulas
        self.pose = np.zeros((2, 2))

        l0_pose = np.linalg.multi_dot([self.R[0], self.T[0]])
        l1_pose = np.linalg.multi_dot([self.R[0], self.T[0], self.R[1], self.T[1]])

        self.pose[:, 0] = l0_pose[:, 2][:2]
        self.pose[:, 1] = l1_pose[:, 2][:2]

    def _update_transformation_matrices(self, q0, q1):
        """
        Este método calcula las matrices de rotación traslación del modelo de nuestro robot
        y guarda sus valores como elementos de las listas self.R y self.T, en orden
        """
        q0 = q0 * np.pi / 180
        q1 = q1 * np.pi / 180

        self.q = [q0, q1]

        self.T = []
        self.R = []

        angulo_rotacion_l0 = q0
        angulo_rotacion_l1 = q1

        # Link 1
        self.T.append(translation_along_x_axis(self.a[0]))
        self.R.append(rotation_around_zaxis(angulo_rotacion_l0))
        # Link 2
        self.T.append(translation_along_x_axis(self.a[1]))
        self.R.append(rotation_around_zaxis(angulo_rotacion_l1))

    def inverse_kinematics(self, x, y):
        ## pa q el robot vaya a x,y,x hay q usar
        # q0,q1,q2=inversekinematics
        ##robot.updatepose(q0,q1,q2)

        a1 = self.a[0]
        a2 = self.a[1]
        lim = a1 + a2
        r = np.sqrt(x ** 2 + y ** 2)

        if (r > lim):
            return self.q

        phi0 = np.arctan2(y, x)
        phi1 = np.arccos((r ** 2 + a1 ** 2 - a2 ** 2) / (2 * r * a1))
        phi2 = np.arccos((a1 ** 2 + a2 ** 2 - r ** 2) / (2 * a1 * a2))

        q0 = phi0 - phi1
        q1 = np.pi - phi2

        return np.array([q0, q1]) * 180 / np.pi

    def get_joint_positions(self):
        """Este método entrega las coordenadas de cada joint en 1 listas; es para que el codigo se vea mas limpio :)"""

        X_pos = self.pose[0]
        Y_pos = self.pose[1]

        return [X_pos, Y_pos]

    def get_pose_error(self, inputed_coord):

        x, y = inputed_coord
        xr, yr = self.pose[:, 1]
        error_x = np.abs(x - xr) / x
        error_y = np.abs(y - yr) / y
        return [error_x, error_y]

    def angle_to_step(self, qarr):
        "qarr must be in degres"
        q0, q1 = qarr
        s1 = q0 * 200
        s2 = q1 * 400
        self.s = [s1, s2]

        return self.s

    def write_coords_as_gcode(self, file, coords):
        """Takes an array of tuples with coordinates (in degrees) and writes
        them as Gcode to a file"""

        arch = open(file, 'w')
        for i in range(len(coords)):
            x = str(np.round(coords[i][0], 1))
            y = str(np.round(coords[i][1], 1))
            msg = 'G0 X' + x + ' Y' + y + '\n'  # G0 Xx Yy
            arch.write(msg)

        arch.close()

    def move_linear_sim(self, start, end, speed):
        xs, ys = start
        xt, yt = end
        move_dist = np.sqrt((xs - xt) ** 2 + (ys - yt) ** 2)
        move_time = move_dist / speed
        

