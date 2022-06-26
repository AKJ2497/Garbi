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
percentage =0

bio =0
non_bio =0

airquality = 0
CO2_sensor = 0

grovepi.pinMode(pir_sensor,"INPUT")
pinMode(led, "OUTPUT")
pinMode(Relay_pin,"OUTPUT")

time.sleep(1)

while True:
        
        # Sense motion, usually human, within the target range
		motion = grovepi.digitalRead(pir_sensor)
		if motion==0 or motion==1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
			if motion==1:
				print ('Motion Detected')
			else:
				print ('-')

			 # if your hold time is less than this, you might not see as many detections
		    time.sleep(.2)

         # Read distance value from Ultrasonic
         distance = ultrasonicRead(ultrasonic_ranger)
         print(distance,'cm')
         if distance <= 10:
            digitalWrite(Relay_pin,1)
         else:
            digitalWrite(Relay_pin,0)
            
         [ temp, hum ] = dht(dht_sensor_port,1)
         print ("temp=", temp, "C\thumadity =", hum, "%")
         t = str(temp)
         h = str(hum)

         #setRGB(0,128,64)
         #setRGB(0,255,0)
         #setText("Temp:" + t + "C" + "Humidity:" + h + "%")

         digital.Write(led,1)
         time.sleep(1)
         digital.Write(led,0)
         time.sleep(1)

         a = random.randint(0,9)
         print(a)

         if a%2 == 0:
         bio = 1 #motor ON, Display Biodegradable, servo moves to bio bucket

         else:
         non_bio = 1 #motor OFF, Display Non-Biodegradable, servo moves to Non-bio bucket
    
        def servo(state):
        print("Servo :"+str(state))
        if(str(state)=='off'):
        SetAngle(0) 
        bio_distance = ultrasonicRead(ultrasonic_ranger)
         print(bio_distance,'cm')
        
        if(str(state)=='on'):
        SetAngle(180) 
        nonbio_distance = ultrasonicRead(ultrasonic_ranger)
         print(nonbio_distance,'cm')

        def fan(speed):
         print("Fan :"+str(speed))
    
         if(str(speed)=='off'):
         GPIO.output(23,GPIO.LOW)      
         if(str(speed)=='low'):
             GPIO.output(23,GPIO.HIGH)
         if(str(speed)=='medium'):
            GPIO.output(23,GPIO.HIGH)
         if(str(speed)=='high'):
            GPIO.output(23,GPIO.HIGH)


         if CO2_sensor <= 50:
            print('Air Quality is good') #ventillation on low speed, show on dashboard
         else:
            print('Air Quality is bad') #turn on ventillation, call the fan function


     #except (IOError, TypeError) as e:
        #print "Error"
