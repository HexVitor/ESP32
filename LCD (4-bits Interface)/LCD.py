# Project:  LCD module for ESP32
# Author:   João Vítor Carvalho (HexVitor)
# Email:    ejoaocarvalho@gmail.com
# Date:     Dec 26, 2019
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
from time import sleep_ms, sleep_us

# HD44780 LCD controller command set

# basics
_CLEAR_DISPLAY = 0x01         # 0b000001 clear display (and return home)
_GO_HOME = 0x02               # 0b000010 return to home position (0,0)

# entry mode set
_CURSOR_SLIDE_LEFT = 0x04     # 0b000100 write and slide cursor to left
_DISPLAY_SLIDE_RIGHT = 0x05   # 0b000101 write and slide cursor to right
_CURSOR_SLIDE_RIGHT = 0x06    # 0b000110 write and slide display to right
_DISPLAY_SLIDE_LEFT = 0x07    # 0b000111 write and slide display to left

# display on/off control
_HIDE_DISPLAY = 0x08          # 0b001000 turn display off
_BLINK_ON = 0x09              # 0b001001 turn blinking cursor on (mask)
_UNDERSCORE_ON = 0x0A         # 0b001010 turn underscore cursor on (mask)
_SHOW_DISPLAY = 0x0C          # 0b001100 turn display on (no underscore/blinking cursor) (mask)

# cursor or display shift
_CURSOR_SHIFT_LEFT = 0x10     # 0b010000 shift cursor to left
_CURSOR_SHIFT_RIGHT = 0x14    # 0b010100 shift cursor to right
_DISPLAY_SHIFT_LEFT = 0x18    # 0b011000 shift display to left
_DISPLAY_SHIFT_RIGHT = 0x1C   # 0b011100 shift display to right

# function set
_DISPLAY_INIT = 0x32          # 0b110010 init display
_BUS_4_BITS = 0x20            # 0b100000 4 bits (1 line and 5x8 dots by default)
_MASK_2_LINES = 0x08          # 0b--1000 2 lines mask
_MASK_5x10_DOTS = 0x04        # 0b--0100 5x10 dots mask

# staff
_LINE_0 = 0x80                # 1st line initial adress (0,0)
_LINE_1 = 0xC0                # 2nd line initial adress (1,0)
_MASK_LINE_0_2 = 0x00
_MASK_LINE_1_3 = 0x01
_DISPLAY_STATUS = False
_UNDERSCORE_STATUS = False
_BLINK_STATUS = False


class LCD:

    def __init__(self, rs, en, d4, d5, d6, d7):
        
        
        # set pins
        self.RS = Pin(rs, Pin.OUT, value = 0)
        self.EN = Pin(en, Pin.OUT, value = 0)
        self.D4 = Pin(d4, Pin.OUT, value = 0)
        self.D5 = Pin(d5, Pin.OUT, value = 0)
        self.D6 = Pin(d6, Pin.OUT, value = 0)
        self.D7 = Pin(d7, Pin.OUT, value = 0)
        
        self.digits = 0
        self.lines = 0


    def begin(self, digits = 16, lines = 2):
        
        self.send(_DISPLAY_INIT)
        sleep_ms(5)
        
        if digits > 40: self.digits = 40
        else: self.digits = digits
        print(self.digits)
        
        if lines > 4: self.lines = 4
        else: self.lines = lines
        print(self.lines)
        
        if self.lines == 1: self.send(BUS_4_BITS)
        else: self.send(_BUS_4_BITS | _MASK_2_LINES)
        sleep_ms(1)
        
        self.send(_CURSOR_SLIDE_RIGHT)
        sleep_ms(1)
        self.show_display()
        sleep_ms(1)
        self.clear()
        sleep_ms(1)


    def clear(self):
        
        self.send(_CLEAR_DISPLAY)


    def home(self):
        
        self.send(_GO_HOME)


    def show_display(self):
        
        if _UNDERSCORE_STATUS == False and _BLINK_STATUS == False: self.send(_SHOW_DISPLAY)
        if _UNDERSCORE_STATUS == False and _BLINK_STATUS == True: self.send(_SHOW_DISPLAY | _BLINK_ON)
        if _UNDERSCORE_STATUS == True and _BLINK_STATUS == False: self.send(_SHOW_DISPLAY | _UNDERSCORE_ON)
        if _UNDERSCORE_STATUS == True and _BLINK_STATUS == True: self.send(_SHOW_DISPLAY | _UNDERSCORE_ON | _BLINK_ON)
        
        global _DISPLAY_STATUS
        _DISPLAY_STATUS = True


    def hide_display(self):
        
        self.send(_HIDE_DISPLAY)
        
        global _DISPLAY_STATUS
        _DISPLAY_STATUS = False


    def write(self, data):
        
        width = len(data)
        for i in range(width): self.send(ord(data[i]), 1)


    def set_cursor(self, go_digit, go_line):
        
        if go_line | _MASK_LINE_0_2 == False:
            if go_digit < self.digits: self.send(_LINE_0 | go_digit)
            else: self.send(_LINE_0 | self.digits)
            
        if go_line & _MASK_LINE_1_3 == True:
            if go_digit < self.digits: self.send(_LINE_1 | go_digit)
            else: self.send(_LINE_1 | self.digits)


    def underscore(self):

        if _DISPLAY_STATUS == False and _BLINK_STATUS == False: self.send(_UNDERSCORE_ON)
        if _DISPLAY_STATUS == False and _BLINK_STATUS == True: self.send(_UNDERSCORE_ON | _BLINK_ON)
        if _DISPLAY_STATUS == True and _BLINK_STATUS == False: self.send(_SHOW_DISPLAY | _UNDERSCORE_ON)
        if _DISPLAY_STATUS == True and _BLINK_STATUS == True: self.send(_SHOW_DISPLAY | _UNDERSCORE_ON | _BLINK_ON)
        
        global _UNDERSCORE_STATUS
        _UNDERSCORE_STATUS = True

    def no_underscore(self):
        
        if _DISPLAY_STATUS == False and _BLINK_STATUS == False: self.send(_HIDE_DISPLAY)
        if _DISPLAY_STATUS == False and _BLINK_STATUS == True: self.send(_BLINK_ON)
        if _DISPLAY_STATUS == True and _BLINK_STATUS == False: self.send(_SHOW_DISPLAY)
        if _DISPLAY_STATUS == True and _BLINK_STATUS == True: self.send(_SHOW_DISPLAY | _BLINK_ON)
        
        global _UNDERSCORE_STATUS
        _UNDERSCORE_STATUS = False


    def blink(self):
        
        if _DISPLAY_STATUS == False and _UNDERSCORE_STATUS == False: self.send(_BLINK_ON)
        if _DISPLAY_STATUS == False and _UNDERSCORE_STATUS == True: self.send(_BLINK_ON | _UNDERSCORE_ON)
        if _DISPLAY_STATUS == True and _UNDERSCORE_STATUS == False: self.send(_SHOW_DISPLAY | _BLINK_ON)
        if _DISPLAY_STATUS == True and _UNDERSCORE_STATUS == True: self.send(_SHOW_DISPLAY | _BLINK_ON | _UNDERSCORE_ON)
        
        global _BLINK_STATUS
        _BLINK_STATUS = True


    def no_blink(self):
        
        if _DISPLAY_STATUS == False and _UNDERSCORE_STATUS == False: self.send(_HIDE_DISPLAY)
        if _DISPLAY_STATUS == False and _UNDERSCORE_STATUS == True: self.send(_UNDERSCORE_ON)
        if _DISPLAY_STATUS == True and _UNDERSCORE_STATUS == False: self.send(_SHOW_DISPLAY)
        if _DISPLAY_STATUS == True and _UNDERSCORE_STATUS == True: self.send(_SHOW_DISPLAY | _BLINK_ON | _UNDERSCORE_ON)
        
        global _BLINK_STATUS
        _BLINK_STATUS = False


    def blink_display(self, times, time_up = 500, time_down = 500):
        
        for i in range(times):
            lcd.hide_display()
            sleep_ms(time_down)
            lcd.show_display()
            sleep_ms(time_up)


    def shift_display(self, times):
        
        for i in range(times):
            self.send(_DISPLAY_SHIFT_LEFT)
            sleep_ms(500)
        sleep_ms(1000)
        for i in range(times):
            self.send(_DISPLAY_SHIFT_RIGHT)


    def send(self, bits, mode = 0):
        
        # bits = instruction
        # mode: 0 = command, 1 = character
        
        self.RS.value(mode)
        
        # high bits
        self.D4.value(0)
        self.D5.value(0)
        self.D6.value(0)
        self.D7.value(0)
        
        if bits & 0x10 == 0x10: self.D4.value(1)   # &: binary AND
        if bits & 0x20 == 0x20: self.D5.value(1)
        if bits & 0x40 == 0x40: self.D6.value(1)
        if bits & 0x80 == 0x80: self.D7.value(1)
        
        # toggle 'enable' pin (LCD read high bits)
        self.toggle_enable()
        
        # low bits
        self.D4.value(0)
        self.D5.value(0)
        self.D6.value(0)
        self.D7.value(0)
        
        if bits & 0x01 == 0x01: self.D4.value(1)
        if bits & 0x02 == 0x02: self.D5.value(1)
        if bits & 0x04 == 0x04: self.D6.value(1)
        if bits & 0x08 == 0x08: self.D7.value(1)
        
        # toggle 'enable' pin (LCD read low bits)
        self.toggle_enable()


    def toggle_enable(self):
        
        # toggle enable
        sleep_us(500)
        self.EN.value(1)
        sleep_us(500)
        self.EN.value(0)
        sleep_us(500)

# test
lcd = LCD(13, 12, 14, 27, 26, 25)
lcd.begin()
lcd.write("It works!")
