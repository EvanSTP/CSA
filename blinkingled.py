#!/usr/bin/env python3.0
# Blinking LED Project
# LED blinks 10 times ar a rate of 1 per second

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

counter = 0
duration = 0.25

while counter != 100:
##    print(counter)
##    GPIO.output(18, 1)
##    time.sleep(0.5)
##    GPIO.output(18, 0)
##    time.sleep(0.1)
##    counter+=1
    
    t_end = time.time() + duration
    while time.time() <= t_end:
        GPIO.output(18, True)
    GPIO.output(18, False)
    GPIO.output(23, True)
    time.sleep(0.25)
    GPIO.output(23, False)
    counter += 1
    if counter%10 == 0:
        print(counter)

GPIO.cleanup()
        

        
