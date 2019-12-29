# 28BYJ-48 Stepper Motor module
MicroPython 28BYJ-48 stepper motor module for ESP32 (ULN2003 Driver Interface)
<p align = "center">
  <img src = "https://github.com/HexVitor/ESP32/blob/master/Media/28BYJ-48_connection_example.png" alt = "28BYJ-48 connection example" />
</p>

## Environment

The code was generated and tested in the following environment:

```
PC:  Raspberry Pi 3B
OS:  Raspbian 10 Buster
IDE: Thonny Python IDE 3.2.0
MCU: ESP-WROOM-32 (chip ESP32D0WDQ6, revision 1)
uOS: MicroPython v1.11 (2019-10-26)
Mod: 28BYJ-48 Stepper Motor and ULN2003 Driver
```

## How to use:

1. Connect your ULN2003 Driver to ESP32 pins 23(IN1), 22(IN2), 21(IN3) and 19(IN4).

2. Power the ULN2003 with an external power supply (5V~12V)

3. With Thonny Python IDE, create a new empty file, copy and paste the code on BYJ.py into this file and run it.

3. If all works well, your 28BYJ-48 stepper motor will rotate 90 degrees and then do a full rotation.
```
Yeah!
```

## Functions

To create an object:
```
object_name = BYJ(IN1, IN2, IN3, IN4)
```

Other functions:
```
rotate_degree(degrees, direction)
rotate_turn(turns, direction)
# direction '0': clockwise, direction '1': counter-clockwise
# if no direction is specified, the rotation will be clockwise
# speed ~ 15 RPM
```

## Built With

[Thonny Python IDE](https://thonny.org/) - Python IDE for beginners

## Author

**Vítor Carvalho** [HexVitor](https://github.com/HexVitor) *based on [**Gaven MacDonald**](https://www.youtube.com/channel/UCfMxbH6WR35780HqCw7eDiA) video: [Stepper Motor Control with the Raspberry Pi](https://www.youtube.com/watch?v=Dc16mKFA7Fo)*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details