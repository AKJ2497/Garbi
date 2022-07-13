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
               "airquality": 0}

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
mqttc_sd.on_message_sd = on_message_sd                               # assign on_message func
mqttc_sd.connect('192.168.0.145', 1883, 60)
mqttc_sd.loop_start()

while 1==1:
	time.sleep(2)
	if connflag == True:
		temprature = sensor_data["temp"]
		airquality = sensor_data["airquality"]
		print("temp:", temperature , "airquality: ", airquality)
	else:
		print("waiting for connection....")


