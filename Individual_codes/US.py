import time
from datetime import datetime
from grovepi import *

ultra_1 = 4
ultra_2 = 6
percentage = 0

def US_S1(dist_1):
        print(dist_1,'cm')
   	#if dist_1 <= 10:
            #digitalWrite(Relay_pin,1) 
        #else:
            #digitalWrite(Relay_pin,0)
		 	
def US_bin_selection(dist):                                          #Read distance value from Ultrasonic
        print("Bin Distance=" , dist, "cm")
	percentage = 100 * (6 - dist)/6
	print("Bin Status=" , percentage, "%")
	if percentage >= 80:
		print("Bin is 80% full, Please change the Bin!")
   	

while True:

	distance = ultrasonicRead(ultra_1)
	bin_depth = ultrasonicRead(ultra_2)
	US_S1(distance)
	US_bin_selection(bin_depth)
	time.sleep(1)


	