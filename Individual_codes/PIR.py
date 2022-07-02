import time
from datetime import datetime
from grovepi import *
from grove_rgb_lcd import *

pir_sensor = 8
led =5
pinMode(pir_sensor,"INPUT")
pinMode(led, "OUTPUT")

while True:
	try:
		motion = digitalRead(pir_sensor)
		if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
			if motion==1:
				print ('Human Motion Detected')
				digitalWrite(led,1)
				time.sleep(5) #turn on lights when human is present

			else:
				print ('-')
				digitalWrite(led,0) #turn off lights
                

	except KeyboardInterrupt:
		digitalWrite(led,0) 
		break

	except (IOError, TypeError) as e:
		print ("Error")

	