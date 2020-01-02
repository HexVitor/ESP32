# Project:  LCD module for ESP32 (I2C Interface)
# Author:   João Vítor Carvalho (HexVitor)
# Email:    ejoaocarvalho@gmail.com
# Date:     Dec 27, 2019
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

# for cursor location
_LINE_0 = 0x80                # 1st line initial adress (0,0)
_LINE_1 = 0xC0                # 2nd line initial adress (1,0)
_MASK_LINE_0_2 = 0x00
_MASK_LINE_1_3 = 0x01

# auxiliary variables
_RS = 0x01
_EN = 0x04
_COMMAND = 0
_CHARACTER = 1
_BACKLIGHT_ON = bytearray([0x08])
_BACKLIGHT_OFF = bytearray([0x00])

# control variables
_DISPLAY_STATUS = False
_UNDERSCORE_STATUS = False
_BLINK_STATUS = False

class LCD_I2C():
    
    def __init__(self, bus, addr, digits, lines):
        
        self.i2c = bus
        self.addr = addr
        
        self.partial_delivery(_DISPLAY_INIT)
        sleep_ms(5)
        self.partial_delivery(_DISPLAY_INIT)
        sleep_ms(1)
        self.partial_delivery(_DISPLAY_INIT)
        sleep_ms(1)
        
        self.partial_delivery(_BUS_4_BITS)
        
        self.digits = 0
        self.lines = 0
        self.backlight = False
        
        if digits > 40: self.digits = 40
        else: self.digits = digits
        
        if lines > 4: self.lines = 4
        else: self.lines = lines
        
        if self.lines > 1: self.send(_BUS_4_BITS | _MASK_2_LINES)
        self.send(_CURSOR_SLIDE_RIGHT)
        self.backlight_on()
        self.show_display()
        self.clear()


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


    def backlight_on(self):
        
        self.backlight = True
        self.i2c.writeto(self.addr, _BACKLIGHT_ON)


    def backlight_off(self):
        
        self.backlight = False
        self.i2c.writeto(self.addr, _BACKLIGHT_OFF)


    def write(self, data):
        
        width = len(data)
        for i in range(width): self.send(ord(data[i]), _CHARACTER)


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
            self.hide_display()
            sleep_ms(time_down)
            self.show_display()
            sleep_ms(time_up)


    def shift_display(self, times):
        
        for i in range(times):
            self.send(_DISPLAY_SHIFT_LEFT)
            sleep_ms(500)
        sleep_ms(1000)
        for i in range(times):
            self.send(_DISPLAY_SHIFT_RIGHT)

    def send(self, bits, mode = _COMMAND):
        
         # 'self.backlight << 3' set 0x08 if backlight is 1

        if mode == _COMMAND:
            
            HSB = bits & 0xF0
            LSB = (bits & 0x0F) << 4
            BACKLIGHT_STATUS = self.backlight << 3
            packet_1 = bytearray([HSB | BACKLIGHT_STATUS | _EN])
            packet_2 = bytearray([HSB | BACKLIGHT_STATUS])
            packet_3 = bytearray([LSB | BACKLIGHT_STATUS | _EN])
            packet_4 = bytearray([LSB | BACKLIGHT_STATUS])
            self.full_delivery(packet_1, packet_2, packet_3, packet_4)
            
        if mode == _CHARACTER:
            
            HSB = bits & 0xF0
            LSB = (bits & 0x0F) << 4
            BACKLIGHT_STATUS = self.backlight << 3
            packet_1 = bytearray([HSB | BACKLIGHT_STATUS | _EN | _RS])
            packet_2 = bytearray([HSB | BACKLIGHT_STATUS | _RS])
            packet_3 = bytearray([LSB | BACKLIGHT_STATUS | _EN | _RS])
            packet_4 = bytearray([LSB | BACKLIGHT_STATUS | _RS])
            self.full_delivery(packet_1, packet_2, packet_3, packet_4)


    def partial_delivery(self, command):
        
        raw_byte = (command >> 4) << 4
        packet_1 = bytearray([raw_byte | _EN])
        packet_2 = bytearray([raw_byte])
        self.i2c.writeto(self.addr, packet_1)
        self.i2c.writeto(self.addr, packet_2)


    def full_delivery(self, packet_1, packet_2, packet_3, packet_4):
        
        # for i2c at 100KHz doesn't need sleep_us
        # for i2c at 400KHz it needs at least 150us between sending
        self.i2c.writeto(self.addr, packet_1)
        sleep_us(150)
        self.i2c.writeto(self.addr, packet_2)
        sleep_us(150)
        self.i2c.writeto(self.addr, packet_3)
        sleep_us(150)
        self.i2c.writeto(self.addr, packet_4)
        sleep_us(150)


# test
from machine import I2C
i2c = I2C(0) # scl = Pin(18), sda = Pin(19), freq = 400KHz
addr = i2c.scan()[0]
lcd = LCD_I2C(i2c, addr, 16, 2)
lcd.write("it works!")
lcd.blink()
