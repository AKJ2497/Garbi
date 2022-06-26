# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from flask import Flask, render_template, url_for, request, redirect, make_response
# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import json
from time import time

sensor_data = {"temp": 0,
               "humid": 0,
               "light": 0,
               "fan": "off",
               "servo": "off",
               "led": "0"}

app: Flask = Flask(__name__)


def on_connect(client, userdata, flags, rc):  # func for making connection
    print("Connection returned result: " + str(rc))
    client.subscribe([("Sensor_Data", 1), ("Actions", 1)])


def on_message(client, userdata, msg):  # Func for receiving msgs
    a = msg.topic
    if a == "Sensor_Data":
        t = json.loads(str(msg.payload.decode("utf-8")))
        sensor_data["temp"] = t["Temperature"]
        sensor_data["humid"] = t["Humidity"]
        sensor_data["light"] = t["Light_Intensity"]
    if a == "Actions":
        t = json.loads(str(msg.payload.decode("utf-8")))
        for key, value in t.items():
            if key == "Fan":
                sensor_data["fan"] = t["Fan"]
            if key == "Servo":
                sensor_data["servo"] = t["Servo"]
            if key == "LED":
                sensor_data["led"] = t["LED"]






mqttc = paho.Client()  # mqttc object
mqttc.on_connect = on_connect  # assign on_connect func
mqttc.on_message = on_message  # assign on_message func
# mqttc.on_log = on_log
#### Change following parameters ####
#awshost = "xxxxxxxxxxxxxx-ats.iot.<region>.amazonaws.com"  # Endpoint
#awsport = 8883  # Port no.
clientId = "Rpi_Visual"  # Thing_Name
thingName = "Rpi_V"  # Thing_Name
caPath = "certificates/AmazonRootCA1.pem"  # Root_CA_Certificate_Name
certPath = "certificates/certificate.pem.crt"  # <Thing_Name>.cert.pem
keyPath = "certificates/private.pem.key"  # <Thing_Name>.private.key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)

mqttc.connect(awshost, awsport, keepalive=60)  # connect to aws server


mqttc.loop_start()
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
        Light = int(sensor_data["light"])
        LED = str(sensor_data["led"])
        Servo = str(sensor_data["servo"])
        Fan = str(sensor_data["fan"])
        data = [time() * 1000, Temperature, Humidity, Light, Fan, LED, Servo]

        response = make_response(json.dumps(data))

        response.content_type = 'application/json'

        return response


    if __name__ == "__main__":
        app.run(debug=True)