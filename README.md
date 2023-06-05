# Pico-Daylight
Authors:<br>
Andrew Macpherson (@admacpherson)<br>
Mark Clemmer (@mclemmer7)<br>
Ebby Buchta (@ebbyy)<br>
Handrae Henthorn<br><br>
<img src="https://user-images.githubusercontent.com/29272159/134868586-bd05f5e9-eaf2-4ac2-9688-7aca16165bf8.png" width="250">

## Description
This repository hosts the files for our Raspberry Pi Pico project for a Daylight Alarm<br>

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

<b>Special Consideration: WiFi Captive Portal: </b>
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
