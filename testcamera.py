#!/usr/bin/python

# use this to test camera 

import RPi.GPIO as GPIO
import os, datetime, errno, picamera

from time import sleep

button_pin = 21   # button pin
delay = 1

camera = picamera.PiCamera()

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Press the button to take a picture")

while True:
    is_pressed = GPIO.wait_for_edge(button_pin, GPIO.FALLING, timeout=100)

    if is_pressed is None:
        continue

    print("Button pressed")
    camera.start_preview()
    sleep(2)
    camera.stop_preview()
    camera.capture("/home/pi/Desktop/test.jpg")

GPIO.cleanup()
