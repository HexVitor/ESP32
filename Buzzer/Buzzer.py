# Project:  Buzzer module for ESP32
# Author:   João Vítor Carvalho (HexVitor)
# Email:    ejoaocarvalho@gmail.com
# Date:     Dec 28, 2019
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

from machine import Pin, PWM
from time import sleep_ms

# note set

NOTE_B0 = 31
NOTE_C1 = 33
NOTE_CS1 = 35
NOTE_D1 = 37
NOTE_DS1 = 39
NOTE_E1 = 41
NOTE_F1 = 44
NOTE_FS1 = 46
NOTE_G1 = 49
NOTE_GS1 = 52
NOTE_A1 = 55
NOTE_AS1 = 58
NOTE_B1 = 62
NOTE_C2 = 65
NOTE_CS2 = 69
NOTE_D2 = 73
NOTE_DS2 = 78
NOTE_E2 = 82
NOTE_F2 = 87
NOTE_FS2 = 93
NOTE_G2 = 98
NOTE_GS2 = 104
NOTE_A2 = 110
NOTE_AS2 = 117
NOTE_B2 = 123
NOTE_C3 = 131
NOTE_CS3 = 139
NOTE_D3 = 147
NOTE_DS3 = 156
NOTE_E3 = 165
NOTE_F3 = 175
NOTE_FS3 = 185
NOTE_G3 = 196
NOTE_GS3 = 208
NOTE_A3 = 220
NOTE_AS3 = 233
NOTE_B3 = 247
NOTE_C4 = 262
NOTE_CS4 = 277
NOTE_D4 = 294
NOTE_DS4 = 311
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_FS4 = 370
NOTE_G4 = 392
NOTE_GS4 = 415
NOTE_A4 = 440
NOTE_AS4 = 466
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_CS5 = 554
NOTE_D5 = 587
NOTE_DS5 = 622
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_FS5 = 740
NOTE_G5 = 784
NOTE_GS5 = 831
NOTE_A5 = 880
NOTE_AS5 = 932
NOTE_B5 = 988
NOTE_C6 = 1047
NOTE_CS6 = 1109
NOTE_D6 = 1175
NOTE_DS6 = 1245
NOTE_E6 = 1319
NOTE_F6 = 1397
NOTE_FS6 = 1480
NOTE_G6 = 1568
NOTE_GS6 = 1661
NOTE_A6 = 1760
NOTE_AS6 = 1865
NOTE_B6 = 1976
NOTE_C7 = 2093
NOTE_CS7 = 2217
NOTE_D7 = 2349
NOTE_DS7 = 2489
NOTE_E7 = 2637
NOTE_F7 = 2794
NOTE_FS7 = 2960
NOTE_G7 = 3136
NOTE_GS7 = 3322
NOTE_A7 = 3520
NOTE_AS7 = 3729
NOTE_B7 = 3951
NOTE_C8 = 4186
NOTE_CS8 = 4435
NOTE_D8 = 4699
NOTE_DS8 = 4978
REST = 0

# Buzzer module to sing notes or melodies

class Buzzer():
    
    def __init__(self, pin):
        
        self.pin = PWM(Pin(pin), freq=0, duty=0)


    def sing(self, melody, bpm):
        
        notes = len(melody)
        
        for note in range(0, notes, 2): # notes index are even while duration index are odd
            
            divider = melody[note + 1]
            whole_note = (60000 * 4) / bpm
            
            if divider > 0: duration = whole_note / divider               # common notes (standart time)
            if divider < 0: duration = (whole_note / abs(divider)) *1.5   # dotted notes (standard time + his half time)
            
            self.tone(melody[note], int(duration))


    def tone(self, note, duration = 0):
        
        self.pin.duty(20)
        
        if duration > 0:
            
            # play a note with duration
            self.pin.freq(note)
            sleep_ms(duration)
            
            self.pin.duty(0)


        else:
            self.pin.freq(note)


    def no_tone(self):
        
        # power off PWM signal
        self.pin.duty(0)
        bz.freq(0)

# Ode to Joy - Beethoven's Symphony No. 9
ode_to_joy = [
        
    NOTE_E4, 4, NOTE_E4, 4, NOTE_F4, 4, NOTE_G4, 4,
    NOTE_G4, 4, NOTE_F4, 4, NOTE_E4, 4, NOTE_D4, 4,
    NOTE_C4, 4, NOTE_C4, 4, NOTE_D4, 4, NOTE_E4, 4,
    NOTE_E4, -4, NOTE_D4, 8, NOTE_D4, 2,
    
    NOTE_E4, 4, NOTE_E4, 4, NOTE_F4, 4, NOTE_G4, 4,
    NOTE_G4, 4, NOTE_F4, 4, NOTE_E4, 4, NOTE_D4, 4,
    NOTE_C4, 4, NOTE_C4, 4, NOTE_D4, 4, NOTE_E4, 4,
    NOTE_D4, -4, NOTE_C4, 8, NOTE_C4, 2,
    
    NOTE_D4, 4, NOTE_D4, 4, NOTE_E4, 4, NOTE_C4, 4,
    NOTE_D4, 4, NOTE_E4, 8, NOTE_F4, 8, NOTE_E4, 4, NOTE_C4, 4,
    NOTE_D4, 4, NOTE_E4, 8, NOTE_F4, 8, NOTE_E4, 4, NOTE_D4, 4,
    NOTE_C4, 4, NOTE_D4, 4, NOTE_G3, 2,
    
    NOTE_E4, 4, NOTE_E4, 4, NOTE_F4, 4, NOTE_G4, 4,
    NOTE_G4, 4, NOTE_F4, 4, NOTE_E4, 4, NOTE_D4, 4,
    NOTE_C4, 4, NOTE_C4, 4, NOTE_D4, 4, NOTE_E4, 4,
    NOTE_D4, -4, NOTE_C4, 8, NOTE_C4, 2
    
    ]


# test
buzzer = Buzzer(4)
buzzer.sing(ode_to_joy, 114)