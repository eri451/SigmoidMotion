#!/usr/bin/env python

import socket
import math
import time
from struct import *

class SigmoidMotion:
    HOST   = '172.22.99.206'
    PORT   = 2342
    s      = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    colorA = {"red":0x66, "green":0xCC, "blue":0x00}
    colorB = {"red":0xCC, "green":0x66, "blue":0x00}
    # header
    data   = [pack('b',0x0F), pack('b',0), pack('!h',678)]
    # east side LEDs
    left   = pack('BBB',colorA["blue"], colorA["green"], colorA["red"])
    # west side LEDs
    right  = pack('BBB',colorB["blue"], colorB["green"], colorB["red"])

    period = 3000         # five minutes
    transitionLength = 40 # four seconds

    maxRuntime = 36000    # sixty minutes


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
            lred   = self.ramp(self.colorA["red"],   self.colorB["red"],   time)
            lgreen = self.ramp(self.colorA["green"], self.colorB["green"], time)
            lblue  = self.ramp(self.colorA["blue"],  self.colorB["blue"],  time)

            rred   = self.ramp(self.colorB["red"],   self.colorA["red"],   time)
            rgreen = self.ramp(self.colorB["green"], self.colorA["green"], time)
            rblue  = self.ramp(self.colorB["blue"],  self.colorA["blue"],  time)

            self.left  = pack('BBB', lblue, lgreen, lred)
            self.right = pack('BBB', rblue, rgreen, rred)
        else:
            rred   = self.ramp(self.colorA["red"],   self.colorB["red"],   time)
            rgreen = self.ramp(self.colorA["green"], self.colorB["green"], time)
            rblue  = self.ramp(self.colorA["blue"],  self.colorB["blue"],  time)

            lred   = self.ramp(self.colorB["red"],   self.colorA["red"],  time)
            lgreen = self.ramp(self.colorB["green"], self.colorA["green"], time)
            lblue  = self.ramp(self.colorB["blue"],  self.colorA["blue"],  time)

            self.left  = pack('BBB', lblue, lgreen, lred)
            self.right = pack('BBB', rblue, rgreen, rred)

    def __call__(self):
        globaltimer = 0
        timer = 0
        epoch = 0
        asc = True
        while globaltimer < self.maxRuntime:
            globaltimer = globaltimer + 1
            timer = timer + 1
            if timer < self.period:
                self.s.sendto(self.packet(),(self.HOST,self.PORT))
                time.sleep(0.09)
                continue
            elif timer == self.period:
                epoch = timer
                self.transition(timer-epoch, asc)
            elif timer > self.period and timer < self.period + self.transitionLength:
                self.transition(timer-epoch, asc)
            else:
                asc = not asc
                timer = 0

            self.s.sendto(self.packet(),(self.HOST,self.PORT))
            time.sleep(0.08)

        s.close()

if __name__ == '__main__':
    sigmo = SigmoidMotion()
    sigmo()
