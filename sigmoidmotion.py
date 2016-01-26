#!/usr/bin/env python

import socket
import time
from struct import pack


class SigmoidMotion:
    HOST = '172.22.99.206'
    PORT = 2342
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    colorA = {'red': 0x66, 'green': 0xCC, 'blue': 0x00}
    colorB = {'red': 0xCC, 'green': 0x66, 'blue': 0x00}
    # header
    data = [pack('b', 0x0F), pack('b', 0), pack('!h', 678)]
    # east side LEDs
    left = pack('BBB', colorA['blue'], colorA['green'], colorA['red'])
    # west side LEDs
    right = pack('BBB', colorB['blue'], colorB['green'], colorB['red'])

    period = 3000           # five minutes
    transitionLength = 40   # four seconds

    maxRuntime = 36000      # sixty minutes

    def ramp(self, start, end, time):
        fres = start + time*(float(end - start)/self.transitionLength)
        return abs(int(fres))

    def packet(self):
        self.data = [pack('b', 0x0F), pack('b', 0), pack('!h', 678)]
        for i in range(0, 226):
            if i < 3:
                self.data.append(self.right)
            elif i < 13:
                self.data.append(self.left)
            elif i < 19:
                self.data.append(self.right)
            elif i < 120:
                self.data.append(self.left)
            else:
                self.data.append(self.right)
        return ''.join(self.data)

    def transition(self, time, asc):
        left = {}
        right = {}

        if asc:
            colorA = self.colorA
            colorB = self.colorB
        else:
            colorA = self.colorB
            colorB = self.colorA

        for col in ['red', 'green', 'blue']:
            left[col] = self.ramp(colorA[col], colorB[col], time)
            right[col] = self.ramp(colorB[col], colorA[col], time)

        self.left = pack('BBB', left['blue'], left['green'], left['red'])
        self.right = pack('BBB', right['blue'], right['green'], right['red'])

    def __call__(self):
        globaltimer = 0
        timer = 0
        epoch = 0
        transitionEnd = self.transitionLength + self.period
        asc = True
        while globaltimer < self.maxRuntime:
            globaltimer = globaltimer + 1
            timer = timer + 1
            if timer < self.period:
                self.s.sendto(self.packet(), (self.HOST, self.PORT))
                time.sleep(0.09)
                continue
            elif timer == self.period:
                epoch = timer
                self.transition(timer-epoch, asc)
            elif timer > self.period and timer < transitionEnd:
                self.transition(timer-epoch, asc)
            else:
                asc = not asc
                timer = 0

            self.s.sendto(self.packet(), (self.HOST, self.PORT))
            time.sleep(0.08)

        self.s.close()

if __name__ == '__main__':
    sigmo = SigmoidMotion()
    sigmo()
