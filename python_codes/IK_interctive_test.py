import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
from time import sleep
from python_codes.mk2Robot import MK2Robot

""" 1. Useful functions """


def plot_robot(X_pos, Y_pos):
    # Clear figure
    ax.clear()

    # Plot the data
    ax.scatter(0, 0, s=30)  # Origin
    ax.plot([0, X_pos[0]], [0, Y_pos[0]])  # L0
    ax.plot([X_pos[0], X_pos[1]], [Y_pos[0], Y_pos[1]])  # L1
    ax.scatter(X_pos, Y_pos, s=20)  # Joints

    # Make it prettier
    ax.set_ylabel('Y [mm]')
    ax.set_xlabel('X [mm]')

    # Set axis limits
    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)


""" 2. The actual script """

# Spawn a robot!
l1 = 80
l2 = 75
axlength = l1 + l2 + 20

robot = MK2Robot(link_lengths=[l1, l2])

# Create the figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-axlength, axlength)
ax.set_ylim(-axlength, axlength)
ax.set_aspect('equal')

history_len = 100
xdata, ydata = [], []
line, = ax.plot([], [], 'o-', lw=2)
trace, = ax.plot([], [], ',-', lw=1)
history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)

# Plot the robot for the first time


axcolor = 'lightgoldenrodyellow'
ax.margins(x=0)


def gen_circle_points(n, r, dr=0, center=(0, 0)):
    xc, yc = center
    dt = 2 * np.pi / n
    t = 0
    coords = []
    for i in range(n):
        x = r * np.cos(t)
        y = r * np.sin(t)
        coords.append((xc - x, yc - y))
        r += dr
        t += dt

    return np.array(coords)

def gen_square_points(n, l,center):
    xc, yc = center



def gen_x_points(n, l, center=(0, 0)):
    x0, y0 = center
    x = np.linspace(x0 - l * 2 / np.sqrt(2), x0 + l * 2 / np.sqrt(2), n // 2)
    y1 = lambda x: x + y0 - x0
    y2 = lambda x: -x + y0 + x0
    data = []
    for i in range(len(x)):
        data.append((x[i], y1(x[i])))
    for i in range(len(x)):
        data.append((x[i], y2(x[i])))

    return data


def tactoe_grid(box_width, n, center=(0, 0)):
    x0, y0 = center
    l1, l2, l3, l4 = [], [], [], []

    xrange = np.linspace(x0 - int(3 / 2 * box_width), x0 + int(3 / 2 * box_width), n // 4)
    xrangerev = np.linspace(x0 + int(3 / 2 * box_width), x0 - int(3 / 2 * box_width), n // 4)
    yrange = np.linspace(y0 - int(3 / 2 * box_width), y0 + int(3 / 2 * box_width), n // 4)
    yrangerev = np.linspace(y0 + int(3 / 2 * box_width), y0 - int(3 / 2 * box_width), n // 4)

    for i in xrange:
        l1.append((i, y0 + box_width / 2))

    for i in xrangerev:
        l2.append((i, y0 - box_width / 2))

    for i in yrange:
        l3.append((x0 - box_width / 2, i))

    for i in yrangerev:
        l4.append((x0 + box_width / 2, i))

    return l1 + l2 + l3 + l4


def update_frame(i, *coords):
    history_x.clear()
    history_y.clear()

    x, y = coords[i]
    q0, q1 = robot.inverse_kinematics(x, y)
    robot.update_pose(q0, q1)
    [xpos, ypos] = robot.get_joint_positions()
    thisx = [0, xpos[0], xpos[1]]
    thisy = [0, ypos[0], ypos[1]]

    # ax.scatter(x, y, marker='o', color='k')
    xdata.append(xpos[1])
    ydata.append(ypos[1])
    history_x.appendleft(xdata)
    history_y.appendleft(ydata)
    trace.set_data(history_x, history_y)
    line.set_data(thisx, thisy)

    return trace, line,


def gamecoords(center, ngrid, nfig, box_width):
    x0, y0 = center
    d = box_width
    grid = tactoe_grid(box_width, ngrid, center)
    l1, l2, l3, l4, l5, l6, l7, l8, l9 = [], [], [], [], [], [], [], [], []

    indexes = [-1, 0, 1]
    l1 = gen_circle_points(nfig, box_width / 2.5, 0, (x0 - d, y0 + d)).tolist()
    l2 = gen_x_points(nfig, box_width / 3.5, (x0, y0 + d))
    l3 = gen_circle_points(nfig, box_width / 2.5, 0, (x0 + d, y0 + d)).tolist()
    l4 = gen_x_points(nfig, box_width / 3.5, (x0 - d, y0))
    l5 = gen_circle_points(nfig, box_width / 2.5, 0, (x0, y0)).tolist()
    l6 = gen_x_points(nfig, box_width / 3.5, (x0 + d, y0))
    l7 = gen_circle_points(nfig, box_width / 2.5, 0, (x0 - d, y0 - d)).tolist()
    l8 = gen_x_points(nfig, box_width / 3.5, (x0, y0 - d))
    l9 = gen_circle_points(nfig, box_width / 2.5, 0, (x0 + d, y0 - d)).tolist()

    return grid + l1 + l2 + l3 + l4 + l5 + l6 + l7 + l8 + l9


def print_coords_as_cpp_array(coords):
    print('{', end='')
    for i in range(len(coords)):
        print('{' + '{x}, {y}'.format(x=np.round(coords[i][0], 1), y=np.round(coords[i][1], 1)), end='')
        print('},')

    print('}')


def save_ik_as_tuple(coords):
    out = []
    for i in range(len(coords)):
        x = coords[i][0]
        y = coords[i][1]
        out.append(robot.inverse_kinematics(x, y))
    return np.array(out)


def plan_home_to_first_seq_point(seq, home=robot.home_cartesian, points=10):
    """
    plan seq from home to the first point of the sequence
    :param seq: figure points (x, y) tuple [mm]
    :param home: initial point (home in cartesian coords) [mm]
    :param points: number of interpolation pints (int)
    """

    xh, yh = home
    x0, y0 = seq[0]
    y = lambda x: yh + (x - xh) * (y0 - yh) / (x0 - xh)
    dx = (x0 - xh) / points
    for i in range(points):
        xi = xh + i * dx
        yi = y(xi)
        tup_i = (xi, yi)
        seq.insert(i, tup_i)

def return_to_home(seq, home=robot.home_cartesian, points=100):
    xh, yh = home
    x0, y0 = seq[len(seq) - 1]
    y = lambda x: yh + (x - xh) * (y0 - yh) / (x0 - xh)
    dx = (xh - x0) / points
    for i in range(points):
        xi = x0 + i * dx
        yi = y(xi)
        tup_i = (xi, yi)
        seq.append(tup_i)

def coords_as_gcode(coords, speed):
    cmd = "G0 X{} Y{} F{}"
    for i in range(len(coords)):
        x = round(coords[i][0], 2)
        y = round(coords[i][1], 2)
        print(cmd.format(x, y, speed))


coords = gen_circle_points(20, 25, dr=0, center=(50, 90))
coords_as_gcode(coords, 100.0)

# x_coords = gen_x_points(100, 50, center=(0, 100))
tac_coords = tactoe_grid(40, 500, (0, 70))
plan_home_to_first_seq_point(tac_coords,points=100)
return_to_home(tac_coords)

#for i in range(len(tac_coords)):
#    print(tac_coords[i])

game = gamecoords((0, 0), 500, 50, 50)
plan_home_to_first_seq_point(game, points=100)
return_to_home(game)



#ani = FuncAnimation(fig, update_frame, fargs=coords, frames=len(coords), interval=1, blit=True, repeat=False)
#plt.show()

#circle = gen_circle_points(20, 25, center=(40, 100))
#print_coords_as_cpp_array(tactoe_grid(20, 100, (0, 100)))

"""x, y = input("Enter a two value: ").split()
x = float(x)
y = float(y)

q0, q1 = robot.inverse_kinematics(x, y)
print('angulos: q0= ', q0, 'q1= ', q1)
robot.update_pose(q0, q1)
[X_pos, Y_pos] = robot.get_joint_positions()
print('error de posicion= ', robot.get_pose_error([x, y]))
plot_robot(X_pos, Y_pos)
ax.scatter(x, y, marker='o', color='k')"""

# print_coords_as_cpp_array(save_ik_as_tuple(tac_coords))

path = '/gcodes/test.gcode'
#robot.write_coords_as_gcode(path, coords)
