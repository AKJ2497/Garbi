#########################################################################################################################################
################################# GARBI-Smart/Intelligent Garbage Segregation plant #####################################################
### SCIoT GROUP 10 ************** AKSHAY KUMAR JAJU ****************** VEDANT DALVI #####################################################
#########################################################################################################################################
# Importing all the libraries

from __future__ import print_function
from datetime import datetime
import json
import random
import time
import RPi.GPIO as GPIO
from grovepi import *
import paho.mqtt.client as paho
import time
from relay_lib_seeed import *

#########################################################################################################################################
# Declaring variables and pin-outs

ultra_1 = 6
ultra_2 = 4
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

#########################################################################################################################################
##########  MQTT_PAHO_ICOM     ############

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
mqttc.connect('192.168.38.125',1883,keepalive=60)            # connect to pi
mqttc.loop_start() 

#############################################################################################################################################
# Defining setangle for Servo function

def SetAngle(angle):
   servo1.ChangeDutyCycle(2+(angle/18))
   time.sleep(5)
   servo1.ChangeDutyCycle(0)

#############################################################################################################################################
# Defining percentage for Bin Fill Status 
def Percentage(dist):   
    #Read distance value from Ultrasonic
    percentage = 100 * (5 - dist)/5
    return percentage

##########################################################################################################################################
################# Main simulated_actuator code ################
while True:
	try:
		now = datetime.now()
		dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
		dist_1 = ultrasonicRead(ultra_1)
		print("Distance",dist_1)
		if dist_1 <= 2.5:
			time.sleep(2)
			a = random.randint(0,1)
			print("a=",a)
			if a%2 == 0:
				angle = 0
				SetAngle(angle)
				relay_on(1)
				time.sleep(3)
				relay_off(1)
				time.sleep(0.5)
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
				time.sleep(3)
				relay_off(1)
				time.sleep(0.5)
				non_biodist = ultrasonicRead(ultra_2)
				print("Non-Bio Distance=", non_biodist)
				non_biostatus = Percentage(non_biodist)
				print("Non-Bio status=", non_biostatus, "%")
				if non_biostatus >= 80:
					print("Non-Bio Bin is 80% full, Please change the Non-Bio Bin!")
				time.sleep(2)
		else:
			time.sleep(2)
			relay_off(1)

###################### PUBLISHING SENSOR AND ACTION DATA TO SUBSCRIBER VIA BROKER PAHO-MQTT ############################################################
		paylodmsg0 ="{"
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

###################### KEYBOARD INTERRUPT AND SHUTTING OFF ALL THE DEVICES ###############################################################################		
	except KeyboardInterrupt:
		relay_off(1)
		break

	except (IOError, TypeError) as e:
		print("Error")