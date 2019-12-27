# LCD module (I2C Interface)
MicroPython LCD module for ESP32

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

1. connect your I2C module to ESP32 pins 18(scl), 19(sda), VIN(VCC) and GND(GND).

2. With Thonny Python IDE, create a new empty file, copy and paste the code on LCD_I2C.py into this file and run it.

3. if all works well, lcd displays the following message:
```
It works!
```

## Functions

To create an object:
```
object_name = LCD_I2C(bus, i2c_address, digits, lines)
```

Other functions:
```
clear()
home()
show_display()
hide_display()
backlight_on()
backlight_off()
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

**Vítor Carvalho** [HexVitor](https://github.com/HexVitor)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details