#!/usr/bin/env python3.0
# Read a sing button input
# One LED stays on until the button is pressed, second LED stays on while button held down

import RPi.GPIO as GPIO
import time

counter = 0
begin = 0
end = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    GPIO.output(18, True)
    while True:
        if GPIO.input(5):
##            print("Button pressed!")
            counter+=1
            begin = time.time()
            while GPIO.input(5):
                GPIO.output(18, False)
                GPIO.output(23, True)
            time.sleep(0.1)
##            end = time.time()
            print(counter, "No reward!", time.asctime(time.localtime(begin)), " ", time.asctime(time.localtime(end)))
            if counter%10==0: #(time +0.5 - end < 0.25)
                print(counter, "Reward!", time.asctime(time.localtime(begin)), " ", time.asctime(time.localtime(end)))
        else:
##            print("Button not pressed!")
##            end = time.time()
            GPIO.output(23, False)
            GPIO.output(18, True)
        time.sleep(0.05)
finally:
    GPIO.cleanup()
    






##duration = 0.25
##
##while counter != 100:
####    print(counter)
####    GPIO.output(18, 1)
####    time.sleep(0.5)
####    GPIO.output(18, 0)
####    time.sleep(0.1)
####    counter+=1
##    
##    t_end = time.time() + duration
##    while time.time() <= t_end:
##        GPIO.output(18, True)
##    GPIO.output(18, False)
##    GPIO.output(23, True)
##    time.sleep(0.25)
##    GPIO.output(23, False)
##    counter += 1
##    if counter%10 == 0:
##        print(counter)
##
##GPIO.cleanup()
        

        
