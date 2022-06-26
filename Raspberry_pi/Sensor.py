import time
#import RPi.GPIO as IO
from grovepi import *
from grove_rgb_lcd import *

Relay_pin = 2
ultrasonic_ranger = 4
led =5
dht_sensor_port = 7
pir_sensor = 8

motion=0

pinMode(pir_sensor,"INPUT")
pinMode(led, "OUTPUT")
pinMode(Relay_pin,"OUTPUT")

time.sleep(1)

while True:
        
        
        # Sense motion, usually human, within the target range
        motion = digitalRead(pir_sensor)
        if motion==0 or motion==1:  # check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
            if motion==1:
                print ('Motion Detected')
                digitalWrite(led,1)
                
            else:
                print ('-')
                digitalWrite(led,0)

            # if your hold time is less than this, you might not see as many detections
        time.sleep(.2)

         # Read distance value from Ultrasonic
        distance = ultrasonicRead(ultrasonic_ranger)
        print(distance,'cm')
        if distance <= 10:
            digitalWrite(Relay_pin,1)
        else:
            digitalWrite(Relay_pin,0)
            
        [ temp, hum ] = (dht_sensor_port,1)
        print ("temp =", temp, "C\thumadity =", hum, "%")
        t = str(temp)
        h = str(hum)

        setRGB(0,128,64)
        setRGB(0,255,0)
        setText("Temp:" + t + "C " + "Humidity:" + h + "%")


     #except (IOError, TypeError) as e:
        #print "Error"


        

    