# Ultrasonic module (HC-SR04)
MicroPython Ultrasonic module for ESP32
<p align = "center">
  <img src = "https://github.com/HexVitor/ESP32/blob/master/Media/Ultrasonic_connection_example.png" alt = "Ultrasonic connection example" />
</p>

## Environment

The code was generated and tested in the following environment:

```
PC:  Raspberry Pi 3B
OS:  Raspbian 10 Buster
IDE: Thonny Python IDE 3.2.0
MCU: ESP-WROOM-32 (chip ESP32D0WDQ6, revision 1)
uOS: MicroPython v1.11 (2019-10-26)
Mod: HC-SR04 module
```

## How to use:

1. connect your HC-SR04 module to ESP32 pins VIN(VCC), 21(Trig), 19(Echo) and GND(GND).

2. With Thonny Python IDE, create a new empty file, copy and paste the code on Ultrasonic.py into this file and run it.

3. if all works well, You will see some measurements in the shell!

Ps.: remove the test code before using the module officially.

## Functions

To create an object:
```
object_name = Ultrasonic(trig, echo)
```

Other functions:
```
distance(unit) # unit must be mm, cm or inch
measure() # internal use
```

## Built With

[Thonny Python IDE](https://thonny.org/) - Python IDE for beginners

## Author

**Vítor Carvalho** [HexVitor](https://github.com/HexVitor) based on **Roberto Sánchez** [Roberto](https://github.com/rsc1975) [MicroPython codes](https://github.com/rsc1975/micropython-hcsr04)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details