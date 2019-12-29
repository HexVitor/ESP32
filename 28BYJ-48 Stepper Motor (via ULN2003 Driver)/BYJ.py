# Project:  28BYJ-48 Stepper Motor module for ESP32
# Author:   João Vítor Carvalho (HexVitor)
# Email:    ejoaocarvalho@gmail.com
# Date:     Dec 29, 2019
# License:  MIT

# The MIT License (MIT)
# 
# Copyright (c) 2019 João Vítor de Carvalho Côrtes
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

from machine import Pin
from time import sleep_us

_CW = [ [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 0, 1] ]

_CCW = [ [0, 0, 1, 1],
         [0, 1, 1, 0],
         [1, 1, 0, 0],
         [1, 0, 0, 1] ]


class BYJ:
    
    def __init__(self, in_1, in_2, in_3, in_4):
        
        a = Pin(in_1, Pin.OUT)
        b = Pin(in_2, Pin.OUT)
        c = Pin(in_3, Pin.OUT)
        d = Pin(in_4, Pin.OUT)
        
        self.coils = [a, b, c, d]


    def rotate_degree(self, degrees, direction = 0):
        
        if direction == 0: direction = _CW
        else: direction = _CCW
        
        degrees = int((512/360) * degrees) # 512 cycles per revolution
        
        for i in range(degrees): 
            
            for step in range(4): # 4 steps = 1 revolution (full step mode)
                
                for pin in range(4):
                    self.coils[pin].value(direction[step][pin])
                    
                sleep_us(1950) # 1950us per step ~ 15 RPM

        for pin in range(4):
            self.coils[pin].value(0)


    def rotate_turn(self, turns, direction = 0):
        
        if direction == 0: direction = _CW
        else: direction = _CCW
        
        turns *= 512 # 512 cycles per revolution
        
        for i in range(turns): 
            
            for step in range(4): # 4 steps = 1 revolution (full step mode)
                
                for pin in range(4):
                    self.coils[pin].value(direction[step][pin])
                
                sleep_us(1950) # 1950us per step ~ 15 RPM
                    
        for pin in range(4):
            self.coils[pin].value(0)

# test
from time import sleep

servo = BYJ(23, 22, 21, 19)
servo.rotate_degree(90)
sleep(1)
servo.rotate_turn(1)