from python_codes.defaults import *

class Scara(object):
    def __init__(self, serial_dev):
        self.__serial_dev = serial_dev

    def pen_up(self, ev=None):
        self.__serial_dev.command("M3")

    def pen_down(self, ev=None):
        self.__serial_dev.command("M5")

    def home(self, ev=None):
        self.__serial_dev.command("G1 X81.5 Y82.0 F200.0")

    def set_move_mode(self, absmode):
        if absmode:
            self.__serial_dev.command("G90")
        else:
            self.__serial_dev.command("G91")

    def enable(self):
        self.__serial_dev.command("M17")

    def disable(self):
        self.__serial_dev.command("M84")

    def draw_calibration(self, event=None):
        self.command_gcode(CALIBRATION_PATH)

    def draw_grid(self, event=None):
        self.command_gcode(GRID_PATH)

    def draw_win_line(self, discrete_coords, speed=200.0):
        d_start, d_end = discrete_coords
        x_s, y_s = grid_centers_mm[d_start]
        x_e, y_e = grid_centers_mm[d_end]

        cmd = "G1 X{} Y{} F{}"

        self.enable()
        self.__serial_dev.command(cmd.format(x_s, y_s, speed))
        self.pen_down()
        self.__serial_dev.command(cmd.format(x_e, y_e, speed))
        self.pen_up()
        self.home()
        self.disable()

    def prueba(self, event=None):
        for el in prueba:
            self.draw_win_line(el)

    def draw_fig(self, coords=(0,0), fig_path=X_PATH):
        """
        coords must be the bottom left corner of the X, so we need to convert
        the input (center of box) to bottom left corner
        :param coords: float tuple
        """
        i, j = coords
        x, y = grid_centers_mm[i][j]
        x -= 10.0
        y-= 10.0 # half of cross width
        cmd = "G1 X{} Y{} F{}".format(round(x, 2),
                                      round(y, 2), 200.0)
        self.enable()
        self.__serial_dev.command(cmd)
        self.set_move_mode(False) # set relative mode
        self.command_gcode(fig_path)
        self.set_move_mode(True) # back to abs mode
        self.home()
        self.disable()

    def command_gcode(self, file):
        with open(file) as f:
            while (True):
                line = f.readline().strip('\n')
                if not line:
                    break

                if line[0] == ';':
                    # Comments start with semicolon
                    continue

                self.__serial_dev.command(line)
                #sleep(0.5)

    def command_gcodev2(self, file):
        f = open(file, 'r')
        self.__serial_dev.flushInput()
        for line in f:
            l = line.strip()  # Strip all EOL characters for consistency
            self.__serial_dev.write(l + '\n')  # Send g-code block to grbl
            grbl_out = self.__serial_dev.readline()  # Wait for grbl response with carriage return
            print (' : ' + grbl_out.strip())

