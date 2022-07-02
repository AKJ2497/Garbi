import time
from datetime import datetime
from grovepi import *
from grove_rgb_lcd import *
import random

pir_sensor = 8
led =5
dht_sensor = 7
pinMode(pir_sensor,"INPUT")
pinMode(led, "OUTPUT")
motion=0

def PIR(motion):
        motion = digitalRead(pir_sensor)
	try:
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
		
               
while True:
	[ temp,hum ] = dht(dht_sensor,0)
	time.sleep(2)
	print("temp=", temp, "C/thumidity =", hum,"%")
	t=str(temp)
	h=str(hum)
		
	setRGB(0,128,64)
	setRGB(0,255,0)
	setText("Temp:" + t +"C      " + "Humidity:" + h + "%")

	#temp_value = random.randint(20,50)
	#hum_value = random.randint(0,50)
	#print("Temperature = ", temp_value , "C \tHumidity = ", hum_value, "%") #publish directly to dashboard

	time.sleep(1)
	PIR(pir_sensor)



	