import paho.mqtt.client as paho
import os
import socket
import ssl
import json
from time import sleep
import RPi.GPIO as GPIO
from rpi_ws281x import *
import argparse

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
pwm=GPIO.PWM(17, 50)
pwm.start(0)
emp_count = set()

def SetAngle(angle):
	duty = (angle / 18) + 2
	GPIO.output(17, True)
	pwm.ChangeDutyCycle(duty)

def fan(speed):
    print("Fan :"+str(speed))
    
    if(str(speed)=='off'):
        GPIO.output(23,GPIO.OFF)    
    if(str(speed)=='low'):
        GPIO.output(23,GPIO.LOW)
    if(str(speed)=='medium'):
        GPIO.output(23,GPIO.MEDIUM)
    if(str(speed)=='high'):
        GPIO.output(23,GPIO.HIGH)
    
def servo(state):
    print("Servo :"+str(state))
    if(str(state)=='off'):
        SetAngle(0) 
        
    if(str(state)=='on'):
        SetAngle(180) 
