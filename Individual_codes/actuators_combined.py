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
import requests


sensor_data = {"temp": 0,
               "humid": 0,
               "airquality": 0,
               "fan": "off",
               "led": "ON",
               "alert": 0}

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
    sensor_data["temp"] = s["Temperature"]
    sensor_data["humid"] = s["Humidity"]
    sensor_data["airquality"] = s["Air_Quality"]

mqttc_sd = paho.Client()                                       # mqttc object
mqttc_sd.on_connect_sd = on_connect_sd                               # assign on_connect func
mqttc_sd.on_message_sd = on_message_sd
                               # assign on_message func
mqttc_sd.connect('192.168.0.145', 1883, 80)
 
mqttc_sd.loop_start()

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
#mqttc.connect('192.168.0.145', 1883, 60)            # connect to pi
#mqttc.loop_start() 

#########################################################################################


def SetAngle(angle):
   servo1.ChangeDutyCycle(2+(angle/18))
   time.sleep(5)
   servo1.ChangeDutyCycle(0)  

def Percentage(dist):   
    #Read distance value from Ultrasonic
    percentage = 100 * (6 - dist)/6
    return percentage

def fan1(mode):
    print("Fan1 :"+str(mode))
    if(str(mode)=='off'):
	relay_off(3)
    if(str(mode)=='on'):
	relay_on(3)

def fan2(mode):
    print("Fan2 :"+str(mode))
    if(str(mode)=='off'):
	relay_off(4)
    if(str(mode)=='on'):
	relay_on(4)

              
while True:
	time.sleep(1)
	mqttc.connect('192.168.0.145', 1883, keepalive=60) 
	mqttc.loop_start()
	try:
		if connflag == True:
			now = datetime.now()
			temp = sensor_data["temp"]
			airquality = sensor_data["airquality"]
			print(temp, "-", airquality)
			dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
			
			dist_1 = ultrasonicRead(ultra_1)
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
					time.sleep(2)
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
					time.sleep(2)
					non_biodist = ultrasonicRead(ultra_2)
					print("Non-Bio Distance=", non_biodist)
					non_biostatus = Percentage(non_biodist)
					print("Non-Bio status=", non_biostatus, "%")
					if non_biostatus >= 80:
						print("Non-Bio Bin is 80% full, Please change the Non-Bio Bin!")
					time.sleep(2)
			else:
				relay_off(1)
			"""domain = 'temp_domain.pddl'
			print(domain)
            		if temp < 25:
				fan1("off")
				print("OFF plan created")
                		pb1 = 'temp_pb1.pddl'
				data = {'domain': str(domain),
                        		'problem': str(pb1)}
				resp = requests.post('http://solver.planning.domains/solve',
							verify=False, json=data).json()
				print(resp)
				if str(resp['plan']['result'][0]['name2']) == '(switchonfan temp_high t_high t_high)':
					fan1("off")
					print("OFF plan created")

			elif 25 <= temp <= 70:
				pb2 = 'temp_pb2.pddl'
				data = {'domain': str(domain.decode('utf-8')),
						'problem': str(pb2.decode('utf-8'))}
				resp = requests.post('http://solver.planning.domains/solve',
										verify=False, json=data).json()
				if str(resp['plan']['result'][0]['name2']) == '(switchofffan temp_low t_low t_low)':
					fan1("on")	
					print("ON plan created")
			elif temp > 70:
				digitalWrite(red_led,1)
				digitalWrite(buzzer,1)
				print("FIRE ALERT!")	
			else:
				digitalWrite(red_led,0)
				digitalWrite(buzzer,0) """
			paylodmsg0 ="{"
			paylodmsg1 = "\"datetime\": \""
			paylodmsg2 = "\", \"Bio_Status\":"
			paylodmsg3 = ", \"Nonbio_Status\":"
			paylodmsg4 = "}"
			paylodmsg = "{} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, dt_string, paylodmsg2, biostatus, paylodmsg3, non_biostatus, paylodmsg4)
			paylodmsg = json.dumps(paylodmsg) 
			paylodmsg_json = json.loads(paylodmsg)       
			mqttc.publish("Actuator_Data", paylodmsg_json , qos=1)        # topic: Sensor_Data # Publishing sensor values
			print("msg sent: Data sent" ) # Print sent sensor msg on console
			print(paylodmsg_json)
		
		else:
			print("waiting for connection...")

	except KeyboardInterrupt:
		relay_off(1)
		relay_off(3)
		relay_off(4)
		digitalWrite(buzzer,0)
		digitalWrite(red_led,0)
		break

	except (IOError, TypeError) as e:
		print("Error")