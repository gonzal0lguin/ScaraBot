import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import Slider, Button
from time import sleep


from python_codes.mk2Robot import MK2Robot
from python_codes.SerialDevice import SerialDevice
from python_codes.Robot_driver import Scara

""" 1. Useful functions """

def update(val):
    # This function is called ny time a slider value changes
    #robot.update_pose(q0_slider.val, q1_slider.val)
    [X_pos, Y_pos] = simRobot.get_joint_positions()
    plot_robot(X_pos, Y_pos)
    fig.canvas.draw_idle()


def update_ik(val):
    x = x_slider.val
    y = y_slider.val
    q0, q1 = simRobot.inverse_kinematics(x, y)
    simRobot.update_pose(q0, q1)
    [X_pos, Y_pos] = simRobot.get_joint_positions()
    plot_robot(X_pos, Y_pos)
    str_x = np.round(X_pos[1], 2)
    str_y = np.round(Y_pos[1], 2)
    str_q0 = np.round(q0, 2)
    str_q1 = np.round(q1, 2)
    # print('position [mm]:  x= {} | y= {}'.format(str_x, str_y))
    # print('angle [deg]: q0= {} | q1= {}\n'.format(str_q0, str_q1))
    ax.scatter(x, y, color='k')
    fig.canvas.draw_idle()


def plot_robot(X_pos, Y_pos):
    # Clear figure
    ax.clear()

    # Plot the data
    ax.scatter(0, 0, s=30)  # Origin

    ax.scatter(X_pos, Y_pos, s=20)  # Joints
    ax.plot([X_pos[0], X_pos[1]], [Y_pos[0], Y_pos[1]], linewidth=3)  # L1

    ax.plot(np.linspace(-110, 20, 2), np.ones(2) * 35, 'k')
    ax.plot(np.linspace(-110, 20, 2), np.ones(2) * -35, 'k')
    ax.plot(np.ones(2) * 20, np.linspace(-35, 35, 2), 'k')
    ax.plot(np.ones(2) * -110, np.linspace(-35, 35, 2), 'k')

    ax.plot([0, X_pos[0]], [0, Y_pos[0]], linewidth=3)  # L0

    ax.grid()


    # Make it prettier
    ax.set_ylabel('Y [mm]')
    ax.set_xlabel('X [mm]')

    # Set axis limits
    ax.set_xlim(-160, 160)
    ax.set_ylim(-160, 160)


""" 2. The actual script """

# Spawn a robot!
L1_mm = 81.5
L2_mm = 82.0

simRobot = MK2Robot(link_lengths=[L1_mm, L2_mm])
serial_dev = SerialDevice()
scaraRobot = Scara(serial_dev)

def send_coords(event):
    # Stream g-code to grbl
    x, y = x_slider.val, y_slider.val
    print('Sending: (x= {:.1f}, y= {:.1f})\n'.format(x, y))
    #gcode = str(x) + ',' + str(y) + ','
    gcode = 'G1 X' + str(round(float(x), 2)) + ' Y' + str(round(float(y), 2)) + ' F100.0'
    #print(gcode)

    serial_dev.command(gcode)


def Home_axes(event):
    print('Homing robot...')
    x_slider.reset()
    y_slider.reset()
    send_coords(0)





# Create the figure
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim(-160, 160)
ax.set_ylim(-160, 160)
ax.set_aspect('equal')
# Plot the robot for the first time

simRobot.update_pose(0, 0)  # home pos x= l1, y= l2
[X_pos, Y_pos] = simRobot.get_joint_positions()
plot_robot(X_pos, Y_pos)

axcolor = 'lightgoldenrodyellow'
ax.margins(x=0)

# Adjust the main plot to make room for the sliders
plt.subplots_adjust(bottom=0.4)

# Make horizontal sliders
axx = plt.axes([0.35, 0.25, 0.3, 0.03], facecolor=axcolor)
x_slider = Slider(
    ax=axx,
    label='x [mm]',
    valmin=-160,
    valmax=160,
    valinit=L1_mm,
)

axy = plt.axes([0.35, 0.2, 0.3, 0.03], facecolor=axcolor)
y_slider = Slider(
    ax=axy,
    label='y [mm]',
    valmin=-160,
    valmax=160,
    valinit=L2_mm,
)

"""axq0 = plt.axes([0.35, 0.15, 0.3, 0.03], facecolor=axcolor)
q0_slider = Slider(
    ax=axq0,
    label='q0 [º]',
    valmin=-180,
    valmax=180,
    valinit=0,
)

axq1 = plt.axes([0.35, 0.1, 0.3, 0.03], facecolor=axcolor)
q1_slider = Slider(
    ax=axq1,
    label='q1 [º]',
    valmin=-180,
    valmax=180,
    valinit=90,
)"""

resetax = plt.axes([0.7, 0.075, 0.2, 0.05])
button = Button(resetax, 'Send coordinates', hovercolor='0.975')
pen_btn_up = Button(plt.axes([0.7, .125, 0.1, .05]), 'Pen up', hovercolor='0.975')
pen_btn_dn = Button(plt.axes([0.8, .125, 0.1, .05]), 'Pen down', hovercolor='0.975')
home = Button(plt.axes([0.7, 0.025, 0.2, 0.05]), 'Home axes', hovercolor='0.975')


button.on_clicked(send_coords)
home.on_clicked(Home_axes)
#pen_btn_dn.on_clicked(scaraRobot.pen_down)
pen_btn_dn.on_clicked(scaraRobot.draw_grid)
pen_btn_up.on_clicked(scaraRobot.prueba)

# Add event handler for every slider
x_slider.on_changed(update_ik)
y_slider.on_changed(update_ik)
#q0_slider.on_changed(update)
#q1_slider.on_changed(update)


# Now we are ready to go
plt.show()
