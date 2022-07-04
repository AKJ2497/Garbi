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
biodist =0
non_biodist = 0
biostatus = 0
non_biostatus = 0

GPIO.setmode(GPIO.BOARD)  # Set GPIO numbering mode
GPIO.setup(11,GPIO.OUT)   # Set pin 11 as an output, and define as servo1 as PWM pin
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz
servo1.start(0)         # Start PWM running, with value of 0 (pulse off)

def SetAngle(angle):
   servo1.ChangeDutyCycle(2+(angle/18))
   time.sleep(5)
   servo1.ChangeDutyCycle(0)  

def Percentage(dist):   
    #Read distance value from Ultrasonic
    percentage = 100 * (6 - dist)/6
    return percentage
                 
while True:
	try:
		dist_1 = ultrasonicRead(ultra_1)
		print("Distance",dist_1)
		if dist_1 <= 4:
			relay_on(1)
			relay_on(2)
			a = random.randint(0,1)
			print("a=",a)
			if a%2 == 0:
				angle = 0
				SetAngle(angle)
				time.sleep(3)
				biodist = ultrasonicRead(ultra_2)
				print("Bio Distance=", biodist)
				biostatus = Percentage(biodist)
				print("Bio Status=", biostatus, "%")
				if biostatus >= 80:
					print("Bio Bin is 80% full, Please change the Bio Bin!")
				time.sleep(3)
				
			else:
				angle = 180
				SetAngle(angle)
				time.sleep(3)
				non_biodist = ultrasonicRead(ultra_2)
				print("Non-Bio Distance=", non_biodist)
				non_biostatus = Percentage(non_biodist)
				print("Non-Bio status=", non_biostatus, "%")
				if non_biostatus >= 80:
					print("Non-Bio Bin is 80% full, Please change the Non-Bio Bin!")
				time.sleep(3)
		
		else:
			relay_off(1)
			relay_off(2)

	except KeyboardInterrupt:
		relay_off(1)
		relay_off(2) 
		break

	except (IOError, TypeError) as e:
		print("Error")