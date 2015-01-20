#! /usr/bin/env python

import eyes
import time
import random

class eyes_emot:
    """this class manage eyes expressions."""

    def __init__(self):
        self.eye = eyes.eyes()
        self.openbot = 100
        self.opentop = 100
        self.pupil_offset = [0, 0]
        self.eyebrow_offset = [0, 0]

        random.seed()
        self.nat_loop()


    def blinking(self):
        timer = random.uniform(0, 0.5)
        for bot, top in zip(range((self.openbot + 20), -20, -20), range((self.opentop + 20), -20, -20)):
            self.eye.eye_update([0,0], [0,0], top, bot)
            time.sleep(0.001)
        time.sleep(timer)
        for bot, top in zip(range(0, (self.openbot + 20), 20), range(0, (self.opentop + 20), 20)):
            self.eye.eye_update([0,0], [0,0], top, bot)
            time.sleep(0.001)

    def move_pupil(self):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        timer = random.uniform(0, 1)
        self.eye.eye_update([x,y], self.eyebrow_offset, self.opentop, self.openbot)
        time.sleep(timer)
        self.eye.eye_update(self.pupil_offset, self.eyebrow_offset, self.opentop, self.openbot)

    def move_eyebrow(self):
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        timer = random.uniform(0, 1)
        self.eye.eye_update(self.pupil_offset, [x,y], self.opentop, self.openbot)
        time.sleep(timer)
        self.eye.eye_update(self.pupil_offset, self.eyebrow_offset, self.opentop, self.openbot)

    def nat_loop(self):
        while (1):
            val = random.randint(1, 100)
            if val < 5:
                self.blinking()
            elif val < 15:
                self.move_pupil()
            elif val < 20:
                self.move_eyebrow()
            else:
                time.sleep(0.1)

def main():
    emot = eyes_emot()

if __name__ == "__main__":
    main()
