#!/usr/bin/python

# use this to test if you wired the button correctly.

import RPi.GPIO as GPIO
from time import sleep

button_pin = 21   # button pin
delay = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

i = 1
while i < 4:
  if GPIO.input(button_pin) == False:
    print('Button pushed: ' + str(i))
    sleep(delay)
    i+=1

GPIO.cleanup()
