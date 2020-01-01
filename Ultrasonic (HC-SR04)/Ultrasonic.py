# Project:  HC-SR04 module for ESP32 (Ultrasonic)
# Author:   João Vítor Carvalho (HexVitor)
# Email:    ejoaocarvalho@gmail.com
# Date:     Jan 01, 2020
# License:  MIT

# The MIT License (MIT)
# 
# Copyright (c) 2020 João Vítor de Carvalho Côrtes
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from machine import Pin, time_pulse_us
from time import sleep_ms, sleep_us

# just for support
mm = 'mm'
cm = 'cm'
inch = 'in'

class Ultrasonic():
    
    def __init__(self, trig, echo):
        
        self.trig = Pin(trig, Pin.OUT, value = 0)
        self.echo = Pin(echo, Pin.IN)


    def distance(self, unit):
        
        if unit == mm:
            raw_distance = self.measure() / 2.91 # sound speed: 343.2 m/s = 0.3432 mm/us -> 1 mm in 2.91 us
            
        if unit == cm:
            raw_distance = self.measure() / 29.14 # sound speed: 343.2 m/s = 0.03432 cm/us -> 1 cm in 29.14 us

        if unit == inch:
            raw_distance = self.measure() / 74 # 1 cm in 29.14 us -> 1 inch in 74 us (29.14 * 2.54)
            
        distance = round(raw_distance, 2) # result with 2 decimals
        return distance


    def measure(self):

        # trigger stabilization and actuation
        self.trig.value(0)
        sleep_us(5)
        self.trig.value(1)
        sleep_us(10)
        self.trig.value(0)
        
        # measurement
        double_pulse_time = time_pulse_us(self.echo, 1, 30000) # pin and state to be measured, maximum measurement time
        pulse_time = double_pulse_time / 2 # the pulse walk the distance twice
        return pulse_time


# test
ultrasonic = Ultrasonic(21, 19)

while True:
    print(ultrasonic.distance(cm))
    sleep_ms(500)