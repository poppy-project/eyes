#! /usr/bin/env python

import smbus
import numpy
import time

class led_matrix:
    """this class give access to the led matrix"""

    def __init__(self, lightRatio):
        self.I2C_ADDRESS = [0x70, 0x71, 0x72]
        self.bus = smbus.SMBus(4)
        for i in range(3):
            # start internal oscillator on the LED matrix by sending 0x21 command.
            self.bus.write_byte(self.I2C_ADDRESS[i], 0x21)
            # enable display and turn blink off by sending 0x81.
            self.bus.write_byte(self.I2C_ADDRESS[i], 0x81)
            # set brightness to max by sending 0xEF.
            self.bus.write_byte(self.I2C_ADDRESS[i], (int(lightRatio * 0x0F)) + 0xE0)

            self.mess_send = numpy.ones((3,16), dtype='int32')

        # Create the screen matrix.
        self.clear()
        self.send()

    def __str__(self):
        turned = numpy.rot90(self.screen_mat)
        s = (' ' + '_' * 48) + '\n'
        for y in range(16):
            s += ('|')
            for x in range(24):
                if turned[y][x] > 0:
                    s += (' *')
                else:
                    s += (' .')
            s += ('|\n')
        s += (' ' + '_' * 48) + '\n'
        return s

    def brightness(self, lightRatio):
        for i in range(3):
            # set brightness.
            self.bus.write_byte(self.I2C_ADDRESS[i], (int(lightRatio * 0x0F)) + 0xE0)

    def clear(self):
        self.screen_mat = numpy.zeros((24, 16), dtype='int32')

    def send(self):
        # This function get screen_mat and send it.
        # first off all, cut the main matrix in 3 part 1 for each scenn.
        mats = numpy.split(self.screen_mat, 3)
        for i in range(3):
            mat = numpy.split(numpy.rot90(mats[i]), 2)
            for y in range(16):
                line = 0
                for x in range(8):
                    if mat[1 if (y % 2) else 0][x][(7-(y/2))] > 0:
                        line |= 1 << x
                if self.mess_send[i][y] != line:
                    self.bus.write_byte_data(self.I2C_ADDRESS[i], y, line)
                    self.mess_send[i][y] = line

def main():
    matrix = led_matrix(1.)
    for x in range(1000):
        i = numpy.linspace(0, 1, 24)
        res = (7.9 * numpy.sin(2 * numpy.pi * (i-0.01*x))) + 8
        i = 0
        for a in (res):
            matrix.screen_mat[i][a] = 1
            i += 1
        print chr(27) + "[2J"
        print matrix
        matrix.send()
        matrix.brightness(float(x)/1000.)
        matrix.clear()
        # time.sleep(0.01)

if __name__ == "__main__":
    main()

