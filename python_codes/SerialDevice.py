import serial
import time

BAUD_RATE = 115200
R_TIMEOUT = 60
PORT = '/dev/cu.usbmodem14301'


class SerialDevice(object):
    def __init__(self, __port__=PORT):
        self.__port = __port__
        self.connection = False
        self.serial_dev = None
        self.connect()

    def connect(self):
        try:
            self.serial_dev = serial.Serial(self.__port, BAUD_RATE)
            print('Opening Serial Port')
            self.serial_dev.write(("\r\n\r\n").encode('ascii'))
            time.sleep(2)
            self.serial_dev.flushInput()
            self.connection = True
        except:
            print('Please connect Robot')

    def command(self, data_string):
        if self.connection:
            self.serial_dev.flush()

            self.serial_dev.write((data_string + '\n').encode('ascii'))
            #tnow = time.time()
            last_resp = ''
            #while time.time() - tnow < R_TIMEOUT:
            #if (self.serial_dev.inWaiting() > 0):
            resp = self.serial_dev.readline().strip()
            #if 'ok' in resp:
            #    print(resp)
            #else:
            #    last_resp = resp
            print(resp)
                # if cfg.DEBUG_MODE:
                #    print('serial response:', last_resp)
