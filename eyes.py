#! /usr/bin/env python

import led_matrix
import copy
from eyes_lib import eyes_lib
import time

class eyes:
    """this class Create eyes"""

    def __init__(self, eyes_id=0):
        #init de la matrice led
        self.matrix = led_matrix.led_matrix(1.)
        #Set left eyes origin position (X, Y).
        self.origin = [5,7]
        #Select eyes type.
        self.eye = copy.deepcopy(eyes_lib[eyes_id])
        self.eyeinit = copy.deepcopy(eyes_lib[eyes_id])
        self.eye_update()

    def set_symetry(self):
        for i in range(24):
            self.matrix.screen_mat[23-i] |= self.matrix.screen_mat[i]

    def eye_outline(self):
        # This is the creation af the matrix for the outline of the eyes.
        #Generate one eye matrix
        for x, y in self.eye['bottom']:
            self.matrix.screen_mat[self.eye['positions']['origin'][0] + x][self.eye['positions']['origin'][1] + y] = 1
            self.matrix.screen_mat[23 - (self.eye['positions']['origin'][0] + x)][self.eye['positions']['origin'][1] + y] = 1
        for x, y in self.eye['top']:
            self.matrix.screen_mat[self.eye['positions']['origin'][0] + x][self.eye['positions']['origin'][1] + y] = 1
            self.matrix.screen_mat[23 - (self.eye['positions']['origin'][0] + x)][self.eye['positions']['origin'][1] + y] = 1

    def eyebrow(self):
        # This is the creation af the matrix for the outline of the eyes.
        #Generate one eye matrix
        for x, y in self.eye['eyebrow']:
            self.matrix.screen_mat[self.eye['positions']['eyebrow_center'][0] + x][self.eye['positions']['eyebrow_center'][1] + y] = 1
            self.matrix.screen_mat[23 - (self.eye['positions']['eyebrow_center'][0] + x)][self.eye['positions']['eyebrow_center'][1] + y] = 1

    def eye_pupils(self):
        midl = [self.eye['positions']['pupil_center'][0] + self.eye['positions']['origin'][0],
               self.eye['positions']['pupil_center'][1] + self.eye['positions']['origin'][1]]
        midr = [(midl[0] + 13), midl[1]]
        for x,y in self.eye['pupil']:
            #find the eyelead position
            for topx, topy in self.eye['top']:
                for botx, boty in self.eye['bottom']:
                    if (self.eye['positions']['origin'][0] + topx) == (midl[0] + x) and ((self.eye['positions']['origin'][1] + topy) > (midl[1] + y)):
                        if (self.eye['positions']['origin'][0] + botx) == (midl[0] + x) and ((self.eye['positions']['origin'][1] + boty) < (midl[1] + y)):
                            self.matrix.screen_mat[midl[0] + x][midl[1] + y] = 1
                    if (23 - self.eye['positions']['origin'][0] + topx) == (13 + midl[0] + x) and ((self.eye['positions']['origin'][1] + topy) > (midl[1] + y)):
                        if (23 - self.eye['positions']['origin'][0] + botx) == (13 + midl[0] + x) and ((self.eye['positions']['origin'][1] + boty) < (midl[1] + y)):
                            self.matrix.screen_mat[midr[0] + x][midr[1] + y] = 1

    def eye_update(self, pupil_offset=[0, 0], eyebrow_offset=[0, 0], opentop=100, openbot=100):
        for index, value, in enumerate(self.eyeinit['top']):
            self.eye['top'][index][1] = value[1] * opentop / 100
        for index, value, in enumerate(self.eyeinit['bottom']):
            self.eye['bottom'][index][1] = value[1] * openbot / 100
        self.eye['positions']['pupil_center'] = [self.eyeinit['positions']['pupil_center'][0] + pupil_offset[0],
                                                 self.eyeinit['positions']['pupil_center'][1] + pupil_offset[1]]
        self.eye['positions']['eyebrow_center'] = [self.eyeinit['positions']['eyebrow_center'][0] + eyebrow_offset[0],
                                                   self.eyeinit['positions']['eyebrow_center'][1] + eyebrow_offset[1]]

        self.matrix.clear()
        self.eye_outline()
        self.eyebrow()
        self.eye_pupils()
        self.matrix.send()
        print chr(27) + "[2J"
        print self.matrix

def main():
    eye = eyes()
    while(1):
        for ratio in range(120, -20, -20):
            eye.eye_update([0,0], [0,0], ratio, ratio)
            time.sleep(0.001)
        for ratio in range(0, 120, 20):
            eye.eye_update([0,0], [0,0], ratio, ratio)
            time.sleep(0.001)
        time.sleep(1)

    # for ratio in range(0, 110, 10):
    #     for i in range(5):
    #         eye.eye_update([i,0], ratio, ratio)
    #         time.sleep(0.01)
    #     for i in range(4,-1,-1):
    #         eye.eye_update([i,0], ratio, ratio)
    #         time.sleep(0.01)
    #     for i in range(0, -5, -1):
    #         eye.eye_update([i,0], ratio, ratio)
    #         time.sleep(0.01)
    #     for i in range(-4,1,1):
    #         eye.eye_update([i,0], ratio, ratio)
    #         time.sleep(0.01)

if __name__ == "__main__":
    main()
