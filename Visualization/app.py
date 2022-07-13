#########################################################################################################################################
################################# GARBI-Smart/Intelligent Garbage Segregation plant #####################################################
### SCIoT GROUP 10 ************** AKSHAY KUMAR JAJU ****************** VEDANT DALVI #####################################################
#########################################################################################################################################
# Importing all the libraries

from flask import Flask, make_response, render_template, url_for, request, redirect
import paho.mqtt.client as paho
import json
import time
from time import time

#########################################################################################################################################
# Declaring variables and pin-outs

sensor_data = {"temp": 0,
               "humid": 0,
               "airquality": 0,
               "light": 0,
               "fan": "off",
               "led": "ON",
               "bio": 0,
               "nonbio": 0,
               "alert": 0 }

#########################################################################################################################################
# Visualization Start

app: Flask = Flask(__name__)

#################### SUBSCRIBING SENSOR AND ACTION DATA TO SUBSCRIBER VIA BROKER PAHO-MQTT ###############################################

def on_connect(client, userdata, flags, rc):  # func for making connection
    print("Connection returned result: " +str(rc))
    #client.subscribe([("Sensor_Data", 1), ("Actuator_Data", 1), ("Actions", 1)])
    client.subscribe([("Sensor_Data", 1), ("Actuator_Data", 1)])

def on_message(client, userdata, msg): # Func for receiving msgs
    a = msg.topic
    if a == "Sensor_Data":
        t = json.loads(str(msg.payload.decode("utf-8")))
        sensor_data["temp"] = t["Temperature"]
        sensor_data["humid"] = t["Humidity"]
        sensor_data["airquality"] = t["Air_Quality"]
        
    if a == "Actuator_Data":
        t = json.loads(str(msg.payload.decode("utf-8")))
        sensor_data["bio"] = t["Bio_Status"]
        sensor_data["nonbio"] = t["Nonbio_Status"]

mqtt_subscriber= paho.Client()
mqtt_subscriber.on_message= on_message
mqtt_subscriber.on_connect= on_connect

mqtt_subscriber.connect("192.168.0.145", 1883, 60)
  
mqtt_subscriber.loop_start()
#############################################################################################################################################
# Rendering of Dashboard

while 1 == 1:
    @app.route('/', methods=["GET", "POST"])
    def main():
        return render_template('base.html')


    @app.route('/data', methods=["GET", "POST"])
    def data():
        # Data Format
        # [TIME, Temperature, Humidity]

        Temperature = int(sensor_data["temp"])
        Humidity = int(sensor_data["humid"])
        Airquality = int(sensor_data["airquality"])
        Biobinstatus = int(sensor_data["bio"])
        Nonbiobinstatus = int(sensor_data["nonbio"])
        Light = int(sensor_data["light"])
        #Fan = str(sensor_data["fan"])
        #data = [time() * 1000, Temperature, Humidity, Airquality, Light, Fan, Servo, Safetyalertsystem]
        print("TEMP=", Temperature, "HUM=", Humidity, "AQ=", Airquality, "Bio=", Biobinstatus, "Nbio=", Nonbiobinstatus)
        data = [time() * 1000, Temperature, Humidity, Airquality, Biobinstatus, Nonbiobinstatus, Light]
        print(data)

        response = make_response(json.dumps(data))

        response.content_type = 'application/json'

        return response

    if __name__ == "__main__":
        app.run(debug=True)