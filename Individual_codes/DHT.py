import time
from datetime import datetime
from grovepi import *
from grove_rgb_lcd import *

dht_sensor_port = 7

while True:
	try:
		[ temp,hum ] = dht(dht_sensor_port,0)
		time.sleep(2)
		print("temp=", temp, "C/thumidity =", hum,"%")
		t=str(temp)
		h=str(hum)
		
		setRGB(0,128,64)
		setRGB(0,255,0)
		setText("Temp:" + t +"C      " + "Humidity:" + h + "%")
	
	except (IOError, TypeError) as e:
		print("Error")

