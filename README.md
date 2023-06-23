# Circadian Rhythm Alarm Clock

## Description
This repository hosts the files for our Raspberry Pi Pico project for a Circadian Rhythm Alarm Clock. The system is designed to help one's circadian rhythm more in sync with the natural daylight cycle by mimicking natural light throughout the day. The brightness of the light can be controlled at any time by the user using a dial, which is a potentiometer that scales the user's input to adjust the brightness of the lights on a 0 - 100 scale. The project also has a built in alarm that can wake the user up using soft simulated sunlight that gradually gets brighter. At the end of the wake-up sequence a buzzer is programmed to sound so that the user is sure to be woken. The alarm can be configured to go off at any time, and is able to be turned off for days that you just want to use the clock features. The system has an LCD that displays the current local time, which it fetches using an Internet connection, provided by an ESP8266-01 Wifi Module. <br><br>

The neopixel.py library is required to get the LED strip working, and the RGB1602.py library is used to get the LCD display working.

<b>Features: </b> LED Simulated Daylight, LED Alarm, Buzzer Alarm, OLED, WiFi Connection, Adjustable Brightness
<br><br><img src="https://user-images.githubusercontent.com/29272159/134868586-bd05f5e9-eaf2-4ac2-9688-7aca16165bf8.png" width="250">

## Authors
Andrew Macpherson (@admacpherson)<br>
Mark Clemmer (@mclemmer7)<br>
Ebby Buchta (@ebbyy)<br>
Handrae Henthorn<br><br>

## Our Setup
<img src = "https://github.com/mclemmer7/Pico-Daylight/assets/94164990/fc0644bf-baae-441b-b80a-ee5e06676e66" width="800">


## ESP 8266-01 Documentation
To get the current time for the alarm clock, our project uses an ESP8266-01 Wifi module to connect to the Internet and the MicroPython `utime` library to fetch the present time. 

### Wiring
The wiring of the ESP8266-01 to the Raspberry Pi Pico is as follows:

<b>ESP ........... Pico</b><br>
3v3 ........... 3v3 (via breadboard positive rail)<br>
RST ........... <i>N/A</i><br>
EN  ........... 3v3 (via breadboard positive rail)<br>
TX  ........... GP0<br>
RX  ........... GP1<br>
IG1 ........... <i>N/A</i><br>
IG2 ........... <i>N/A</i><br>
GND ........... GND (optional via breadboard negative rail)<br>
<img src="https://github.com/admacpherson/Pico-Daylight/assets/102562791/64283c5c-97bb-4aaf-80ca-152729058106" width="350">


### Software
Prerequisite: MicroPython for Raspberry Pi Pico must be installed on the device. Our version (rp2-pico-20230426-v1.20.0.uf2) is available in the repository.

Our program uses a modified version of Noyel Seth's (@noyelseth) <a href="https://github.com/Circuit-Digest/rpi-pico-micropython-esp8266-lib">rpi-pico-micropython-esp8266-lib</a>. Many thanks to @MladenSU for their crucial <a href="https://github.com/Circuit-Digest/rpi-pico-micropython-esp8266-lib/pull/1">pull request</a> that fixes fatal errors.<br>

The `esp8266time.py` file contains three main sections
1. HTTP Parser Class
2. ESP 8266 Class
3. Main Program

The main program first sets up the ESP8266-01 module as an instantiated Python object, then connects to the local Wifi network given the username and password, and finally gets and returns the local time.<br>

<b>Instantiating the ESP8266 object: </b> The `esp8266.py` class contains a default class constructor:
`def __init__(self, uartPort=0, baudRate=115200, txPin=(0), rxPin=(1))`. Before changing the TX and RX pins, consult the <a href="https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html">Raspberry Pi Pico documentation</a> to ensure that the UART port does not also need to be changed.

<img width="600" alt="Screenshot 2023-06-06 at 11 02 01 AM" src="https://github.com/admacpherson/Pico-Daylight/assets/102562791/642abab4-ed45-4748-88b2-8626c3658a33">


<b>Special Consideration - WiFi Captive Portal: </b>
Our primary workspace was located on-campus at Seattle Pacific University. Accordingly, we relied largely on campus WiFi which does not use traditional WPA-2 encryption as is found on many home and business networks. Instead, SPU relies on a captive portal which allows any user to join the network with a simple username and password but does not provide Internet connection until the user is authenticated via a login to an SPU webpage. Obviously the Pico is not a browser device so to account for this we followed <a href="https://wiki.spu.edu/display/HKB/Registering+Non-Browser+Devices+for+Network+Access">the instructions</a> of the CIS Helpdesk at SPU, which require opening a port for the device based on its MAC address. To do this, we connected the ESP8266-01 to CoolTerm and performed the following process:

1. Configure settings<br>
a. Ensure correct port is selected<br>
b. Set Baudrate: 115200<br>
c. Enable line mode via Settings > Terminal Options > Line Mode
2. Ensure the ESP8266-01 is properly connected by sending `AT` via the terminal<br>
a. A response of "OK" means it is working<br>
b. Anything else means the module is not properly connected<br>
3. Set station mode with `AT+CWMODE=1`
4. Get MAC address with `AT+CIPSTAMAC?`
5. <i>Optional: The WiFi can be connected directly via terminal using `AT+CWJAP=“SSID”,”Password”` (include quotes)</i>

## Final Comments
We were able to connect the Raspberry Pi Pico to WiFi with the ESP8266 module, but were not able to get the current time from the internet. The current time is the only thing that is effected by this and it will start at 12:00 AM every time it recieves battery power. If the alarm clock is plugged into a laptop, it will recieve the current time.
