
import pika
import time
from datetime import datetime
from grovepi import *
from grove_rgb_lcd import *
import random
import RPi.GPIO as GPIO
#import paho.mqtt.client as paho
import json




####################################
port = 7
sensor = 0
timeout=1
  

pir_sensor = 8
led = 5
dht_sensor = 7

pinMode(pir_sensor,"INPUT")
pinMode(led,"OUTPUT")

motion = 0

###############################################
# config

###############################################
credentials = pika.PlainCredentials('newadmin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.145', 5672, '/', credentials)) 
channel = connection.channel()

channel.exchange_declare(exchange='sciot.topic', exchange_type='topic', durable=True, auto_delete=False) 

####################################################


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
    now = datetime.now()
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    #temp_value = random.randint(20,150)
    #hum_value = random.randint(0,50)
    airquality = random.randint(20,100)

    PIR(pir_sensor)

    [ temp_value,hum_value ] = dht(dht_sensor,0)
    #time.sleep(1)
    t=str(temp_value)
    h=str(hum_value)
    setRGB(0,128,64)
    setRGB(0,255,0)
    #setText("Temp:" + t +"C        " + "Humidity:" + h + "%")
    time.sleep(1)

    paylodmsg0 ="{"
    paylodmsg1 = "\"datetime\": \""
    paylodmsg2 = "\", \"Temperature\":"
    paylodmsg3 = ", \"Humidity\":"
    paylodmsg4= ", \"Air_Quality\":"
    paylodmsg5= "}"
    paylodmsg = "{} {} {} {} {} {} {} {} {} {}".format(paylodmsg0, paylodmsg1, dt_string, paylodmsg2, temp_value, paylodmsg3, hum_value, paylodmsg4, airquality, paylodmsg5)
    paylodmsg = json.dumps(paylodmsg) 
    paylodmsg_json = json.loads(paylodmsg)    
    channel.basic_publish(exchange='sciot.topic', routing_key='u38.0.353.window.temperature.12345', body= paylodmsg_json)    
        # mqttc.publish("Sensor_Data", paylodmsg_json , qos=0)        # topic: Sensor_Data # Publishing sensor values
    print("msg sent: Data sent" ) # Print sent sensor msg on console
    print(paylodmsg_json)
    time.sleep(timeout)