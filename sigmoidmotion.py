#!/usr/bin/env python

import socket
import math
import time
from struct import *

class SigmoidMotion:
    HOST   = '172.22.99.206'
    PORT   = 2342
    s      = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # header
    data   = [pack('b',0x0F), pack('b',0), pack('!h',678)]
    # east side LEDs
    left   = pack('BBB',0x00,0xCC,0x66)
    # west side LEDs
    right  = pack('BBB',0x00,0x66,0xCC)

    period = 3000         # five minutes
    transitionLength = 40 # four seconds


    def ramp(self, start, end, time):
        """ returns value between start and end at given time linary """
        return abs(int(start + time*(float(end - start) / self.transitionLength)))



    def packet(self):
        self.data = [pack('b',0x0F), pack('b',0), pack('!h',678)]
        for i in range(0,226):
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
        return "".join(self.data)


    def transition(self, time, asc):
        if asc:
            self.left  = pack('BBB', 0x00, self.ramp(0xCC,0x66,time), self.ramp(0x66, 0xCC, time))
            self.right  = pack('BBB', 0x00, self.ramp(0x66,0xCC,time), self.ramp(0xCC, 0x66, time))
        else:
            self.left  = pack('BBB', 0x00, self.ramp(0x66,0xCC,time), self.ramp(0xCC, 0x66, time))
            self.right  = pack('BBB', 0x00, self.ramp(0xCC,0x66,time), self.ramp(0x66, 0xCC, time))

    def __call__():
        a = 0
        epoch = 0
        asc = True
        while True:
            a = a + 1
            if a < sms.period:
                sms.s.sendto(sms.packet(),(sms.HOST,sms.PORT))
                time.sleep(0.09)
                continue
            elif a == sms.period:
                epoch = a
                sms.transition(a-epoch, asc)
            elif a > sms.period and a < sms.period + sms.transitionLength:
                sms.transition(a-epoch, asc)
            else:
                asc = not asc
                a = 0

            sms.s.sendto(sms.packet(),(sms.HOST,sms.PORT))
            time.sleep(0.08)

        s.close()

if __name__ == '__main__':
    SigmoidMotion()
