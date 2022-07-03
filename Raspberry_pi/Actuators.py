from __future__ import print_function
from datetime import datetime
import json
import random
import time
import RPi.GPIO as GPIO
from grovepi import *


import sys
import time

from relay_lib_seeed import *


ultra_1 = 4
ultra_2 = 6
a = 0
angle = 90
percentage = 0

GPIO.setmode(GPIO.BOARD)  # Set GPIO numbering mode
GPIO.setup(11,GPIO.OUT)   # Set pin 11 as an output, and define as servo1 as PWM pin
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz
servo1.start(0)         # Start PWM running, with value of 0 (pulse off)

def process_loop():
    # turn all of the relays on
    relay_all_on()
    # wait a second
    time.sleep(15)
    # turn all of the relays off
    relay_all_off()
    # wait a second
    time.sleep(1)

def SetAngle(angle):
   servo1.ChangeDutyCycle(2+(angle/18))
   time.sleep(5)
   servo1.ChangeDutyCycle(0)  
            
		 	
def US_bin_depth(dist, percentage):   
    dist = ultrasonicRead(ultra_2)                             #Read distance value from Ultrasonic
    print("Bin Distance=" , dist, "cm")
    percentage = 100 * (6 - dist)/6
    print("Bin Status=" , percentage, "%")
    if percentage >= 80:
	    print("Bin is 80% full, Please change the Bin!")
     
                                          

try:
    while True:
        dist_1 = ultrasonicRead(ultra_1)
	print("Distance",dist_1)
        if dist_1 <= 4:
            relay_on(1,2)
            time.sleep(10) #see after running conveyor
            relay_off(1,2)

            a = random.randint(0,9)
            print(a)
            if a%2 == 0:
                angle = 0
                SetAngle(angle) #bio
    
            else:
                angle = 180
                SetAngle(angle)  #non_bio


        

finally:
    #Clean things up at the end
    servo1.stop()
    GPIO.cleanup()
    print("Goodbye!")