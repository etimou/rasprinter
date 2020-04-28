#!/usr/bin/python

# This script will wait for a button to be pressed and then shutdown
# the Raspberry Pi (long press) or start a scan (short press)

import time
from time import sleep
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Pin 21 will be input and will have its pull-up resistor (to 3V3) activated
# so we only need to connect a push button with a current limiting resistor to ground
GPIO.setup(37, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# GPIO10 (on pin 23) will be our LED pin
GPIO.setup(23, GPIO.OUT)

GPIO.output(23, GPIO.HIGH)
sleep(1)
GPIO.output(23, GPIO.LOW)

int_active = 0


# ISR: if our button is pressed, we will have a falling edge on pin 21
# this will trigger this interrupt:
def Int_shutdown(channel):

        # button is pressed
        # possibly shutdown our Raspberry Pi

        global int_active

        # only react when there is no other shutdown process running

        if (int_active == 0):

                counter = 0
                while ((GPIO.input(37) == False) and (int_active!=2)):
                        # button is still pressed
                        counter = counter + 1
                        sleep(0.1)
                        if (counter >= 21):
                                int_active = 2

                if (2 <= counter <= 20):
                        int_active = 1
                


# Now we are programming pin 21 as an interrupt input
# it will react on a falling edge and call our interrupt routine "Int_shutdown"
GPIO.add_event_detect(37, GPIO.FALLING,  callback = Int_shutdown, bouncetime = 1000)

# blink once every couple of seconds while waiting for button to be pressed
while 1:

        time.sleep(3)

        # only blink when the button isn't pressed
        # only blink when there's no shutdown in progress
        if (int_active == 0):
                GPIO.output(23, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(23, GPIO.LOW)
                sleep(0.1)
 
        if (int_active == 1):
                GPIO.output(23, GPIO.HIGH)
                print ("Scanning...")
                os.system("/home/pi/scan.bash")
                int_active = 0
                GPIO.output(23, GPIO.LOW)
        if (int_active == 2):
                print ("Shutting down...")
                for i in range (10):
                        GPIO.output(23, GPIO.HIGH)
                        sleep(0.05)
                        GPIO.output(23, GPIO.LOW)
                        sleep(0.05)
                os.system("/sbin/shutdown -h now &")
                for i in range(100):
                        GPIO.output(23, GPIO.HIGH)
                        sleep(0.05)
                        GPIO.output(23, GPIO.LOW)
                        sleep(0.05)
                int_active = 0

# That's all folks!

