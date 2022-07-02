import time
from datetime import datetime
from grovepi import *
from grove_rgb_lcd import *
import random
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import json

connflag = False

def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to Pi")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
mqttc.connect("192.168.0.145", 1883, keepalive=60)               # connect to aws server
mqttc.loop_start() 

pir_sensor = 8
led = 5
ultra_1 = 4
ultra_2 = 6
dht_sensor = 7

pinMode(pir_sensor,"INPUT")
pinMode(led,"OUTPUT")

motion=0
percentage = 0
bio = 0
nonbio = 0
a = 0
angle = 90

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)


def US_S1(dist_1):
        print(dist_1,'cm')
		 	
def US_bin_selection(dist):                                          #Read distance value from Ultrasonic
        print("Bin Distance=" , dist, "cm")
	percentage = 100 * (6 - dist)/6
	print("Bin Status=" , percentage, "%")
	if percentage >= 80:
		print("Bin is 80% full, Please change the Bin!")
   	
def PIR(motion):
        motion = digitalRead(pir_sensor)
	try:
		if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
			if motion==1:
				print ('Human Motion Detected')
				digitalWrite(led,1)
				time.sleep(0.5) #turn on lights when human is present

			else:
				print ('-')
				digitalWrite(led,0) #turn off lights
		
	except KeyboardInterrupt:
		digitalWrite(led,0) 


while 1==1:
	time.sleep(5)
	if connflag == True:
		now = datetime.now()
		dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
		distance = ultrasonicRead(ultra_1)
		bin_depth = ultrasonicRead(ultra_2)
		temp_value = random.randint(20,150)
		hum_value = random.randint(0,50)
		airquality = random.randint(20,100)
	
		PIR(pir_sensor)
		US_S1(distance)
		US_bin_selection(bin_depth)
	
		#[ temp_value,hum_value ] = dht(dht_sensor,0)
		#time.sleep(1)
		t=str(temp_value)
		h=str(hum_value)
		setRGB(0,128,64)
		setRGB(0,255,0)
		setText("Temp:" + t +"C        " + "Humidity:" + h + "%")
		time.sleep(1)

#Fire and Air quality alert to be done by AI PLANNING

		if temp_value >= 100:
			print("Fire in the Garbi Plant: EMERGENCY, RUN FOR YOUR LIFE!") #publish directly to dashboard
			setRGB(0,128,64)
			setRGB(255,0,0)
			setText("EMERGENCY! FIRE ALERT")
			time.sleep(1)

		if airquality >= 50:
			print("Bad Air Quality in the Garbi Plant: EMERGENCY, WEAR MASK") #publish directly to dashboard
			setRGB(0,128,64)
			setRGB(150,127,0)
			setText("EMERGENCY! BAD AIR QUALITY")
			time.sleep(1)
#Untill here

		print("Temperature = ", temp_value , 
			"C \t Humidity = ", hum_value, 
			"% \t Air Quality = ", airquality, "%"
			)
		paylodmsg0="{"
		paylodmsg1 = "\"datetime\": \""
		paylodmsg2 = "\", \"Temperature\":"
		paylodmsg3 = ", \"Humidity\":"
		paylodmsg4= ", \"Air_Quality\":"
		paylodmsg5= "}"
		paylodmsg = "{} {} {} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, dt_string, paylodmsg2, temp_value, paylodmsg3, hum_value, paylodmsg4, airquality, paylodmsg5)
		paylodmsg = json.dumps(paylodmsg) 
		paylodmsg_json = json.loads(paylodmsg)       
		mqttc.publish("Sensor_Data", paylodmsg_json , qos=0)        # topic: Sensor_Data # Publishing sensor values
		print("msg sent: Data sent" ) # Print sent sensor msg on console


		print(paylodmsg_json)
	else:
		print("waiting for connection...")
		