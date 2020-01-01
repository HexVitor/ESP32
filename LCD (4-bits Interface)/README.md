# LCD module (4-bits Interface)
MicroPython LCD module for ESP32
<p align = "center">
  <img src = "https://github.com/HexVitor/ESP32/blob/master/Media/LCD_4bits_connection_example.png" alt = "LCD 4bits connection example" />
</p>

## Environment

The code was generated and tested in the following environment:

```
PC:  Raspberry Pi 3B
OS:  Raspbian 10 Buster
IDE: Thonny Python IDE 3.2.0
MCU: ESP-WROOM-32 (chip ESP32D0WDQ6, revision 1)
uOS: MicroPython v1.11 (2019-10-26)
Mod: HD44780-based 16x2 LCD Display Module
```

## How to use:

1. connect your LCD module to ESP32 pins GND(VS), VIN(VD), 13(RS), 12(E), 14(D4), 27(D5), 26(D6), 25(D7), VIN(A) and GND(K), and pin V0 on the center pin of the potentiometer.

2. With Thonny Python IDE, create a new empty file, copy and paste the code on LCD.py into this file and run it.

3. if all works well, lcd displays the following message:
```
It works!
```

Ps.: remove the test code before using the module officially.

## Functions

To create an object:
```
object_name = LCD(RS, EN, D4, D5, D6, D7)
```

Other functions:
```
begin(digts, lines) # begin() set 16x2 display
clear()
home()
show_display()
hide_display()
write(data)
set_cursor(go_digt, go_line) # begin on (0,0)
underscore()
no_underscore()
blink()
no_blink()
send(command)
toggle_enable()       # internal use
shift_display(times)  # shift display x times
blink_display(times)  # blink display x times
```

## Built With

[Thonny Python IDE](https://thonny.org/) - Python IDE for beginners

## Author

**Vítor Carvalho** [HexVitor](https://github.com/HexVitor) *based on **Dave Hylands** [dhylands](https://github.com/dhylands)  [Python codes](https://github.com/dhylands/python_lcd)*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
