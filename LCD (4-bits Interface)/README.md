# LCD module (4-bits Interface)
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

**Vítor Carvalho** [HexVitor](https://github.com/HexVitor)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details