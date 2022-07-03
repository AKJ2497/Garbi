import time
from datetime import datetime
import paho.mqtt.client as paho
import json
import RPi.GPIO as GPIO
from grovepi import *

ultra_1 = 4
ultra_2 = 6

percentage = 0
biodist = 0
biobin = 0
nonbiodist = 0
nonbiobin = 0
a = 0
angle = 90
percentage = 0

GPIO.setmode(GPIO.BOARD)  # Set GPIO numbering mode
GPIO.setup(11,GPIO.OUT)   # Set pin 11 as an output, and define as servo1 as PWM pin
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz
servo1.start(0)         # Start PWM running, with value of 0 (pulse off)

def setangle(angle):
   servo1.ChangeDutyCycle(2+(angle/18))
            time.sleep(10)
            servo1.ChangeDutyCycle(0)  
            
def US_S1(dist_1):
    print(dist_1,'cm')
		 	
def US_bin_selection(dist, percentage):                                #Read distance value from Ultrasonic
    print("Bin Distance=" , dist, "cm")
    percentage = 100 * (6 - dist)/6
    print("Bin Status=" , percentage, "%")
    if percentage >= 80:
	    print("Bin is 80% full, Please change the Bin!")

def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Actions" , 1 )                       # Subscribe to "Actions" topic

def on_message(client, userdata, msg):                      # Func for receiving msgs
    act = json.loads(str(msg.payload.decode("utf-8")))
    for key, value in act.items():
        if key == "Fan":
            fan(value)
        if key == "Servo":
            servo(value)
        if key == "LED":
            led(value)        
    
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
mqttc.connect("mqtt.eclipseprojects.io", 1883, keepalive=60)               # connect to aws server
mqttc.loop_start()                                          # Start receiving in loop

US_bin_selection(biodist, biobin)