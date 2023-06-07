from neopixel import Neopixel
import utime
import time, sys
import RGB1602
import math
from machine import Pin
from machine import ADC
from machine import PWM

# These modules would be used to get the wifi module to set the correct time, but we couldn't figure it out in the time that we had
# import network, ntptime
# from machine import RTC
# from ntptime import settime

from esp8266time import ESP8266
buzzer = PWM(Pin(14))
button_hours = Pin(2, Pin.IN)
button_minutes = Pin(3, Pin.IN)
button_ampm = Pin(4, Pin.IN)
button_alarm = Pin(5, Pin.IN)
# Global variables for alarm time
# Alarm currently set for 8:00 am
hours = 8
minutes = 0

# am if value is 0, pm if value is 1
ampm = 0
# Alarm is true if it is on, false if it is off
# We need to display this value
alarm = True

#intitialize LCD Display
lcd=RGB1602.RGB1602(16,2)
# Initialize LED

rgb_purp = (148,0,110)
rgb_pink = (255,0,255) 
rgb_green = (144,249,15) 

lcd.setRGB(rgb_green[0],rgb_green[1],rgb_green[2])
time.sleep(0.1)


potentiometer = ADC(26)

# This does connect to the Wifi, but won't give the correct time, so it has been commented out
#-----STARTUP SEQUENCE-----#

# WIFI_NAME = "SPU-Wireless"
# WIFI_PASSWORD = "SPU-Wireless"
# 
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# print("RPi-Pico MicroPython Ver:", sys.version)
# print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# 
# ## Create an ESP8266 Object
# #Default args: uartPort=0, baudRate=115200, txPin=(0), rxPin=(1)
# esp01 = ESP8266()
# esp8266_at_ver = None
# 
# print("StartUP",esp01.startUP())
# print("Echo-Off",esp01.echoING())
# print("\r\n")
# 
# #Print ESP8266 AT comand version and SDK details
# esp8266_at_ver = esp01.getVersion()
# if(esp8266_at_ver != None):
#     print(esp8266_at_ver)
#     
# #-----WIFI CONFIGURATION-----#
# 
# #Set the current WiFi in SoftAP+STA
# print("WiFi Current Mode:",esp01.setCurrentWiFiMode())
# print("\r\n\r\n")
# 
# #Connect with the WiFi
# lcd.printout("Try to connect with the WiFi..")
# while (1):
#     if "WIFI CONNECTED" in esp01.connectWiFi(WIFI_NAME, WIFI_PASSWORD): ###CHANGE WIFI SETTINGS
#         print("ESP8266 connect with the WiFi..")
#         lcd.printout("ESP8266 connected")
# #         rtc = RTC()
# #         from ntptime import settime
# #         ntptime.settime()
# #         response = urequests.get("http://worldtimeapi.org/api/timezone/America/Los_Angeles")
# #         data = response.json()
# #         current_time = data["datetime"]
# #         print(current_time)
#         break;
#     else:
#         print(".")
#         time.sleep(2)
# 
# #-----FUNCTIONALITY-----#
#         
# #Sample HTTP Sequence
# #httpTestSequence()
# 
# # Get the current timestamp in seconds since epoch
# timestamp = utime.time()
# 
# # Convert the timestamp to a tuple representing local time
# local_time = utime.localtime(timestamp)
# 
# # Extract individual components from the local time tuple
# year, month, day, hour, minute, second, _, _ = local_time
# 
# # Print the current date and time
# print("Date: {:04d}-{:02d}-{:02d}".format(year, month, day))
# print("Time: {:02d}:{:02d}:{:02d}".format(hour, minute, second))
# 
# lcd.setCursor(0,0)
# lcd.printout("Time: " + "{:2d}:{:02d}".format(hour, minute))



# This function changes the brightness to the desired
# level as picked up by the potentiometer
def set_brightness():
    value = potentiometer.read_u16()
    lit = round((value - 400)/650)
    strip.brightness(lit)

def print_time():
    # localtime() returns the military time
    current_time = utime.localtime()
    curr_hour = current_time[3]
    curr_minute = current_time[4]
    
    # if hour is between 0 and 11, it is am
    if curr_hour <= 11:
        curr_ampm = "am"
    else:
        curr_ampm = "pm"
        # Make sure that the curr_hour is in standard time instead of military
        curr_hour -= 12
    
    # localtime gives 0 instead of 12
    if curr_hour == 0:
        curr_hour = 12
    
    lcd.setCursor(0,0)
    lcd.printout("Time: " + "{:2d}:{:02d}".format(curr_hour, curr_minute) + curr_ampm)

# This function prints the alarm time on the lcd display
# It will say if the alarm is on or off, and will say if the alarm is set for am or pm
def print_alarm():
    lcd.setCursor(0, 1) # Sets the cursor to the second line to not write over current time
    if alarm:
        alarm_val = "on"
    else:
        alarm_val = "off"
    lcd.printout("Alrm "+ alarm_val + ":{:2d}:{:02d}".format(hours, minutes))
    if ampm == 0:
        lcd.printout("am ")
    else:
        lcd.printout("pm ")


# Increments the number of hours. Hours between 1 and 12
def set_hours():
    global hours
    if hours >= 12:
        hours = 1
    else:
        hours += 1
    # Sleep to deal with bounce
    utime.sleep(0.1)

# Increments the number of minutes by 5 each time. Minutes between 0 and 59 (55 in this case)
def set_minutes():
    global minutes
    increment_val = 1
    minutes += increment_val
    if minutes >= 60:
        minutes -= 60
    # Sleep to deal with bounce
    utime.sleep(0.1)

# This is basically just a toggle between am and pm
def set_ampm():
    global ampm
    if ampm == 0:
        ampm = 1
    else:
        ampm = 0
    # Sleep to deal with bounce
    utime.sleep(0.3)

# This toggles the alarm on and off
def set_alarm():
    global alarm
    if alarm:
        alarm = False
    else:
        alarm = True
    utime.sleep(0.3)

# This is where the code calls the functions that adjust the current time and the alarm time
def timer():
    # Print the current time
    print_time()
    
    # Print the alarm time
    print_alarm()
    
    if button_hours.value() == 1:
        print("Pin hours is on")
        set_hours()
    if button_minutes.value() == 1:
        set_minutes()
        print("Pin minutes is on")
    if button_ampm.value() == 1:
        set_ampm()
        print("Pin ampm is on")
    if button_alarm.value() == 1:
        set_alarm()
        print("Alarm on/off")
    
    utime.sleep(0.1)

# Compares the localtime to the alarm time and returns true if the times are the same
def compare_time():
    current_time = time.localtime()
    curr_hour = current_time[3]
    curr_minute = current_time[4]
    
    # if hour is between 0 and 11, it is am
    if curr_hour <= 11:
        curr_ampm = "am"
        curr_num = 0
    else:
        curr_ampm = "pm"
        curr_num = 1
        curr_hour -= 12
    
    # localtime gives 0 instead of 12
    if curr_hour == 0:
        curr_hour = 12
    
    # Now compare time of current time to alarm time
    if curr_hour == hours:
        if curr_minute == minutes:
            if curr_num == ampm:
                # Alarm will go off now
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# This is the number of pixels on our LED strip
numpix = 144
strip = Neopixel(numpix, 0, 13, "GRB")

# Create colors for the daylight
sunrise1 = (255, 202, 124)
sunrise2 = (255, 210, 140)
sunrise3 = (255, 220, 150)
sunrise4 = (255, 225, 170)
sunrise5 = (255, 230, 190)
sunrise6 = (255, 235, 220)
high_noon = (255, 255, 251)
direct_sunlight = (255, 255, 255)
afternoon1 = (255, 240, 210)
afternoon2 = (255, 225, 160)
afternoon3 = (255, 190, 100)
golden_hour = (255, 147, 41)


colors = [sunrise1, sunrise2, sunrise3, sunrise4, sunrise5, sunrise6, high_noon, direct_sunlight, afternoon1, afternoon2, afternoon3, golden_hour]

# This is the total run time in seconds. It will take a little longner than a minute and a half
time_var = 90
# This array of times holds the percents of the day that each light will be on for
times = [0.05 * time_var, 0.05 * time_var, 0.05 * time_var, 0.05 * time_var, 0.05 * time_var, 0.05 * time_var,
         0.2 * time_var, 0.1 * time_var, 0.05 * time_var, 0.05 * time_var, 0.05 * time_var, 0.25 * time_var]

#Set the base brightness to 50
strip.brightness(50)

# This is where the code is executed, rather than just setting things up
try:
    # Loop through this code until unplugged or stopped
    while True:
        # Checking if alarm is on
        if alarm:
            # compare_time() returns true if the alarm time is equal to current time
            # Continue to loop until the alarm time is met
            while not compare_time():
                timer()
            # Double check to make sure the alarm is still on
            if alarm:
                i = 0  #count variable
                sleep_count = 0   # Keeps track of how long each color has been on for
                # This loop goes through the colors and times arrays to set the color of the LED strip for the given time
                while i < len(colors):
                    # How the buzzer works:
                    #  The lights turn on at the time that the alarm is set for.
                    #  In final product, the buzzer will go off after 10 minutes, but in demo, the buzzer will go off after
                    #  10 seconds if you don't hit the button to turn alarm off.
                    #  When the push button is pressed, it will turn the alarm off
                    # If i equals 3, the buzzer should be activated since the person needs to get up
                    # Turn the buzzer off when alarm is false
                    if i == 3 and alarm:
                        buzzer.freq(930)
                        buzzer.duty_u16(10)
                        utime.sleep(1)
                        buzzer.duty_u16(0)
                        utime.sleep(0.5)
                    
                    set_brightness()
                    # Show the current color on LED strip
                    strip.fill(colors[i])
                    strip.show()
                    
                    # Each loop will take about 0.1 seconds because of this sleep call
                    utime.sleep(0.1)
                    # If sleep_count has reached the end of its time that it should be on for, go to the next color
                    if sleep_count >= times[i]:
                        sleep_count = 0
                        i += 1
                    else:
                        # increment this depending on how many seconds the loop sleeps for
                        sleep_count += 0.2
                    
                    timer()
                # Turn the LED strip off after each whole loop of the cycle
                strip.fill((0, 0, 0))
                strip.show()
        else:
            timer()
        
# Whenever Ctrl+C or STOP is hit, it is a KeyboardInterrupt and this will be executed when that happens
except KeyboardInterrupt:
    print("Program stopped: turning LEDs off.")
    strip.fill((0, 0, 0))
    strip.show()
    lcd.clear()


