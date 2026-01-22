#!/usr/bin/python3
from adafruit_servokit import ServoKit
import time
kit=ServoKit(channels=16)
kit.servo[0].set_pulse_width_range(550,2850)
kit.servo[0].actuation_range=180
    


counter = 0
limit = 0

while counter != 4: 
    kit.servo[0].angle = limit
    limit += 30
    time.sleep(1.5)
##    kit.servo[0].angle = 0
##    time.sleep(0.5)
##    kit.servo[0].angle = 90
##    time.sleep(0.5)
##    kit.servo[0].angle = 70
##    time.sleep(0.5)
    counter +=1
    print (counter, limit)
    

    
