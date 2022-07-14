#########################################################################################################################################
################################# GARBI-Smart/Intelligent Garbage Segregation plant #####################################################
### SCIoT GROUP 10 ************** AKSHAY KUMAR JAJU ****************** VEDANT DALVI #####################################################
#########################################################################################################################################
# Importing all the libraries

from __future__ import print_function
import os
import json
import time
import random
from datetime import datetime
import paho.mqtt.client as paho
from grovepi import *
from grove_rgb_lcd import *
import RPi.GPIO as GPIO
from relay_lib_seeed import *

#########################################################################################################################################
# Declaring variables and pin-outs
connflag = False

pir_sensor = 8
led = 5
dht_sensor = 7
red_led = 2 
buzzer = 3

alert = 0
motion = 0
Fan1 = "off"
Fan2 = "off"

pinMode(pir_sensor,"INPUT")
pinMode(led,"OUTPUT")
pinMode(red_led,"OUTPUT")
pinMode(buzzer,"OUTPUT")

#########################################################################################################################################
##########  MQTT_PAHO_IC     ############

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

########################################################################################################################################
# Defining PIR function
def PIR(motion):
	#motion = digitalRead(pir_sensor)
	if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
		if motion==1:
			print ('Human Motion Detected')
			digitalWrite(led,1)
			time.sleep(0.5)      #turn on lights when human is present
		else:
			print ('NO Human Motion')
			digitalWrite(led,0)  #turn off lights

########################################################################################################################################		
# Reading PDDL plan generated by online Solver
def parseFile(parse):
	lines=[]
	for line in open(parse,'r'):
		lines.append(line)
		len(lines)
		print(lines[0])
		return lines[0]

#######################################################################################################################################
#AI Planner function
def Planner(domainname, problem, out):
	myCmd ='python planning.py {0} {1} {2}'
	myCmd = myCmd.format(domainname, problem, out)
	os.system(myCmd)
	#print(out)
	action = parseFile(out)
	return action

#########################################################################################################################################
# Defining fan1 function
def fan1(mode):
	print("Fan1 :"+str(mode))
	if(str(mode)=='off'):
		relay_off(3)

	if(str(mode)=='on'):
		relay_on(3)

##########################################################################################################################################
# Defining fan2 function

def fan2(mode):
	print("Fan2 :"+str(mode))
	if(str(mode)=='off'):
		relay_off(4)
		
	if(str(mode)=='on'):
		relay_on(4)
		
##########################################################################################################################################
################# Main sensor_actuator code ################

while 1==1:
	try:
		time.sleep(1)
		if connflag == True:
			PIR(pir_sensor)
			now = datetime.now()
			dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
			motion = digitalRead(pir_sensor)
			temp_value = random.randint(20,150)   #Simulated temperature for worst case situation
			hum_value = random.randint(30,100)      #Simulated Humidity for worst case situation
			airquality = random.randint(20,300)	  #Simulated airquality sensor and also for worst case situation		

			#[ temp_value,hum_value ] = dht(dht_sensor,0)  # True Temperature and Humidity from DHT sensor
			#time.sleep(1)

			t=str(temp_value)
			h=str(hum_value)
			setRGB(0,255,0)                        #Displaying on RGB LCD Display   
			setText("Temp:" + t +"C        " + "Humidity:" + h + "%")
			time.sleep(2)

###################### AI PLANNING AND PDDL CALL & SOLVER ################################################################
			domain = 'master_domain.pddl'

			# Temperature PDDL
			if temp_value < 25:
				problem = 'mtemp_pb1.pddl'
				filename = 'mtemp_high.txt'
				fan1_action = Planner(domain, problem, filename)
				print("OFF plan created")
				if str(fan1_action) == "(switchofffan1 temp_low t_low t_low)":
					fan1('off')
					print('relay_off(3)')
				print(fan1_action)
				Fan1 = "off"
			
			elif 25 <= temp_value <= 70:
				problem = 'mtemp_pb2.pddl'
				filename = 'mtemp_low.txt'
				fan1_action = Planner(domain, problem, filename)
				print("ON plan created")
				if str(fan1_action) == "(switchonfan1 temp_high t_high t_high)":
					fan1('on')
					print('relay_on(3)')
				print(fan1_action)
				Fan1 = "on"
			
			else:
				alert = 1
				print("Fire in the Garbi Plant: EMERGENCY, RUN FOR YOUR LIFE!") #publish directly to dashboard
				setRGB(255,0,0)
				setText("EMERGENCY! FIRE ALERT")
				time.sleep(1)
				digitalWrite(red_led,1)
				digitalWrite(buzzer,1)
				time.sleep(2)
				digitalWrite(red_led,0)
				digitalWrite(buzzer,0)
				
			#Air Quality PDDL
			if 100 < airquality <=200:
				problem = 'mAQ_pb1.pddl'
				filename = 'mAQ_fanon.txt'
				fan2_action = Planner(domain, problem, filename)
				print("ON plan created")
				if str(fan2_action) == "(switchonfan2 aq_bad aq_bad aq_bad)":
					fan2('on')
					print('relay_on(4)')
				print(fan2_action)
				Fan2 = "off"

			elif 0<= airquality <=100:
				problem = 'mAQ_pb2.pddl'
				filename = 'mAQ_fanoff.txt'
				fan2_action = Planner(domain, problem, filename)
				print("OFF plan created")
				if str(fan2_action) == "(switchofffan2 aq_good aq_good aq_good)":
					fan2('off')
					print('relay_off(4)')
				print(fan2_action)
				Fan2 = "on"
			else:
				alert =2
				print("Bad Air Quality in the Garbi Plant: EMERGENCY, WEAR MASK") #publish directly to dashboard
				setRGB(120,135,0)
				setText("EMERGENCY! BAD AIR QUALITY")
				time.sleep(1)
				digitalWrite(red_led,1)
				digitalWrite(buzzer,1)
				time.sleep(2)
				digitalWrite(red_led,0)
				digitalWrite(buzzer,0)

			#PIR PDDL
			if motion == 1:
				problem = 'mpir_pb1.pddl'
				filename = 'mpir_yes.txt'
				led_action = Planner(domain, problem, filename)
				print("LED_ON plan created")
				if str(led_action) == "(lighton human_yes pir_yes pir_yes)":
					PIR(1)
					print('led_on')
				print(led_action)
			
			elif motion == 0:
				problem = 'mpir_pb2.pddl'
				filename = 'mpir_no.txt'
				led_action = Planner(domain, problem, filename)
				print("LED_OFF plan created")
				if str(led_action) == "(lightoff human_no pir_no pir_no)":
					PIR(0)
					print('led_off')
				print(led_action)
				
###################### PUBLISHING SENSOR AND ACTION DATA TO SUBSCRIBER VIA BROKER PAHO-MQTT #####################################################################################################
			paylodmsg0 ="{"
			paylodmsg1 = "\"datetime\": \""
			paylodmsg2 = "\", \"Temperature\":"
			paylodmsg3 = ", \"Humidity\":"
			paylodmsg4 = ", \"Fan1\":"
			paylodmsg5 = ", \"Fan2\":"
			paylodmsg6 = ", \"Air_Quality\":"
			paylodmsg7 = ", \"Alert\":"
			paylodmsg8 = "}"
			paylodmsg = "{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, dt_string, paylodmsg2, temp_value, paylodmsg3, hum_value, paylodmsg4, Fan1, paylodmsg5, Fan2, paylodmsg6, airquality, paylodmsg7, alert, paylodmsg8)
			paylodmsg = json.dumps(paylodmsg) 
			paylodmsg_json = json.loads(paylodmsg)       
			mqttc.publish("Sensor_Data", paylodmsg_json , qos=1)        # topic: Sensor_Data # Publishing sensor values
			print("msg sent: Data sent" ) # Print sent sensor msg on console

			print(paylodmsg_json)

		else:
			print("waiting for connection...")

###################### KEYBOARD INTERRUPT AND SHUTTING OFF ALL THE DEVICES #######################################################################################################################

	except KeyboardInterrupt:
		setRGB(0,0,0)
		setText(' ')
		digitalWrite(led,0)
		digitalWrite(red_led,0)
		digitalWrite(buzzer,0)
		relay_all_off()
		break