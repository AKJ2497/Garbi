from __future__ import print_function
from datetime import datetime
import json
import random
import time
import RPi.GPIO as GPIO
from grovepi import *
import paho.mqtt.client as paho
import sys
import time
from relay_lib_seeed import *
import socket


temp = 0
hum  = 0
airquality = 0               
red_led =2
buzzer = 3

ultra_1 = 4
ultra_2 = 6
a = 0
angle = 90
percentage = 0
biodist =0
non_biodist = 0
biostatus = 0
non_biostatus = 0

connflag = False
#temp_value = 0
#airquality = 0
motion = 0
alert = "ALL GOOD"

pinMode(red_led,"OUTPUT")
pinMode(buzzer,"OUTPUT")

GPIO.setmode(GPIO.BOARD)  # Set GPIO numbering mode
GPIO.setup(11,GPIO.OUT)   # Set pin 11 as an output, and define as servo1 as PWM pin
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz
servo1.start(0)         # Start PWM running, with value of 0 (pulse off)

##########################################################################################
##########  MQTT_PAHO_ICOM     ############
def on_connect_sd(client, userdata, flags, rc):  # func for making connection
    print("Connection returned result: " +str(rc))
    client.subscribe("Sensor_Data", 1)

def on_message_sd(client, userdata, msg):
    s = json.loads(str(msg.payload.decode("utf-8")))
    temp = s["Temperature"]
    humid = s["Humidity"]
    airquality = s["Air_Quality"]

mqttc_sd = paho.Client()                                       # mqttc object
mqttc_sd.on_connect_sd = on_connect_sd                               # assign on_connect func
mqttc_sd.on_message_sd = on_message_sd                               # assign on_message func
mqttc_sd.connect('192.168.0.145',1883,keepalive=60) 
mqttc_sd.loop_start()
"""
def on_connect_act(client, userdata, flags, rc):  # func for making connection
    print("Connection returned result: " +str(rc))
    client.subscribe("Actions", 1)

def on_message_act(client, userdata, msg): 
    act = json.loads(str(msg.payload.decode("utf-8")))
    print(act)
    for key, state in act.items():
        if key == "Fan1":
            print(fan(state))
        if key == "Fan2":
            print(servo(state))
        if key == "LED":
            print(led(state))

mqttc_act = paho.Client()                                       # mqttc object
mqttc_act.on_connect_act = on_connect_act                       # assign on_connect func
mqttc_act.on_message_act = on_message_act                       # assign on_message func
mqttc_act.connect('localhost',1883,keepalive=60) 
mqttc_act.loop_start()
"""
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to Pi")
    connflag = True
    print("Connection returned result: " + str(rc))
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
mqttc.connect('192.168.0.145',1883,keepalive=60)            # connect to pi
mqttc.loop_start() 

#########################################################################################


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
	     if connflag == True:
		now = datetime.now()
		dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
		dist_1 = ultrasonicRead(ultra_1)
		print(temp)
		print(airquality)
		print("Distance",dist_1)
		if dist_1 <= 4:
			
			a = random.randint(0,1)
			print("a=",a)
			if a%2 == 0:
				angle = 0
				SetAngle(angle)
				relay_on(1)
				time.sleep(0.15)
				relay_off(1)
				time.sleep(3)
				biodist = ultrasonicRead(ultra_2)
				print("Bio Distance=", biodist)
				biostatus = Percentage(biodist)
				print("Bio Status=", biostatus, "%")
				if biostatus >= 80:
					print("Bio Bin is 80% full, Please change the Bio Bin!")
				time.sleep(1)
				
				
			else:
				angle = 180
				SetAngle(angle)
				relay_on(1)
				time.sleep(0.15)
				relay_off(1)
				time.sleep(3)
				non_biodist = ultrasonicRead(ultra_2)
				print("Non-Bio Distance=", non_biodist)
				non_biostatus = Percentage(non_biodist)
				print("Non-Bio status=", non_biostatus, "%")
				if non_biostatus >= 80:
					print("Non-Bio Bin is 80% full, Please change the Non-Bio Bin!")
				time.sleep(1)
				
		else:
			relay_off(1)
			relay_off(2)
			
		
		if temp < 25:
		   relay_off(3)
		   
	
		elif 25 <= temp <= 70:
		   relay_on(3)
		   	

		else:
		   relay_on(3)
		   alert = "FIRE ALERT!"
		   print(alert)
                   digitalWrite(red_led,1)
                   digitalWrite(buzzer,1)
		   

		if airquality < 25:
		   relay_off(4)
		   
	
		elif 25 <= airquality <= 70:
		   relay_on(4)
		   

		else:
		   relay_on(4)
		   alert = "GAS ALERT!"
		   print(alert)
                   digitalWrite(red_led,1)
                   digitalWrite(buzzer,1)
		   

		paylodmsg0 ="{"
		paylodmsg1 = "\"datetime\": \""
		paylodmsg2 = "\", \"Bio_Status\":"
		paylodmsg3 = ", \"Nonbio_Status\":"
		paylodmsg4 = "}"
		paylodmsg = "{} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, dt_string, paylodmsg2, biostatus, paylodmsg3, non_biostatus, paylodmsg4)
		paylodmsg = json.dumps(paylodmsg) 
		paylodmsg_json = json.loads(paylodmsg)       
		mqttc.publish("Actuator_Data", paylodmsg_json , qos=0)        # topic: Sensor_Data # Publishing sensor values
		print("msg sent: Data sent" ) # Print sent sensor msg on console
		print(paylodmsg_json)

	except KeyboardInterrupt:
		relay_off(1)
		relay_off(3)
		relay_off(4)
		digitalWrite(red_led,0)
		digitalWrite(buzzer,0) 
		break

	except (IOError, TypeError) as e:
		print("Error")