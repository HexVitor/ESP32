# Buzzer module
MicroPython Buzzer module for ESP32
<p align = "center">
  <img src = "https://github.com/HexVitor/ESP32/blob/master/Media/Buzzer_connection_example.png" alt = "Buzzer connection example" />
</p>

## Environment

The code was generated and tested in the following environment:

```
PC:  Raspberry Pi 3B
OS:  Raspbian 10 Buster
IDE: Thonny Python IDE 3.2.0
MCU: ESP-WROOM-32 (chip ESP32D0WDQ6, revision 1)
uOS: MicroPython v1.11 (2019-10-26)
Mod: 5V buzzer module
```

## How to use:

1. connect your buzzer to ESP32 pins 4(VCC) and GND(GND).

2. With Thonny Python IDE, create a new empty file, copy and paste the code on Buzzer.py into this file and run it.

3. if all works well, you will hear Beethoven's Symphony No. 9, Ode to Joy!
```
♫ ♫ Ode to Joy ♫ ♫
```

Ps.: remove the test code before using the module officially.

## Where to find more melodies

1. Visit [arduino songs](https://github.com/robsoncouto/arduino-songs), find the melody note list, copy the notes and their durations (without copy the last comma of the list) and create a new list in your program with them. Maybe you need to remove the comments started with '//'.

## Functions

To create an object:
```
object_name = Buzzer(pin)
```

Other functions:
```
sing(melody, bpm) # melody must be list type
tone(note, duration) # do duration = 0 to unlimited duration
no_tone()
```

## Built With

[Thonny Python IDE](https://thonny.org/) - Python IDE for beginners

## Author

**Vítor Carvalho** [HexVitor](https://github.com/HexVitor) *based on **Robson Couto** [robsoncouto](https://github.com/robsoncouto) [codes for Arduino](https://github.com/robsoncouto/arduino-songs)*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
