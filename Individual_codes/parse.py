from __future__ import print_function
from datetime import datetime
from fileinput import filename
import random
import os

connflag = False
temp_value = 0
airquality = 0
motion = 0
alert = 0

def parseFile(parse):
    lines=[]
    for line in open(parse,'r'):
        lines.append(line)
        len(lines)
        print(lines[0])
        return lines[0]

#AI Planner function

def Planner(domainname, problem, out):
    myCmd ='python planning.py {0} {1} {2}'
    myCmd = myCmd.format(domainname, problem, out)
    os.system(myCmd)
    #print(out)
    action = parseFile(out) #parseFile
    return action


                 
while True:
    try:
        temp_value = random.randint(0,105)
        airquality = random.randint(0,250)
        motion = random.randint(0,1)
        print("temp_value =",temp_value)
        print("AQ =",airquality)
        print("motion =",motion)
        
        #Temperature PDDL
        domain = 'master_domain.pddl'

        if temp_value < 25:
            problem = 'mtemp_pb1.pddl'
            filename = 'mtemp_high.txt'
            fan1_action = Planner(domain, problem, filename)
            print("OFF plan created")
            if str(fan1_action) == "(switchofffan1 temp_low t_low t_low)":
                print('relay_off(3)')
                print(fan1_action)
        
        elif(25 <= temp_value <= 70):
            problem = 'mtemp_pb2.pddl'
            filename = 'mtemp_low.txt'
            fan1_action = Planner(domain, problem, filename)
            print("ON plan created")
            if str(fan1_action) == "(switchonfan1 temp_high t_high t_high)":
                print('relay_on(3)')
                print(fan1_action)
        else:
            alert = 1
            print("FIRE ALERT!")
            

        #Air Quality PDDL

        if 100 < airquality <=200:
            problem = 'mAQ_pb1.pddl'
            filename = 'mAQ_fanon.txt'
            fan2_action = Planner(domain, problem, filename)
            print("ON plan created")
            if str(fan2_action) == "(switchonfan2 aq_bad aq_bad aq_bad)":
                print('relay_on(4)')
                print(fan2_action)
        
        elif 0<= airquality <=100:
            problem = 'mAQ_pb2.pddl'
            filename = 'mAQ_fanoff.txt'
            fan2_action = Planner(domain, problem, filename)
            print("OFF plan created")
            if str(fan2_action) == "(switchofffan2 aq_good aq_good aq_good)":
                print('relay_off(4)')
                print(fan2_action)
        else:
            alert =2
            print("BAD AIR QUALITY!")

        #PIR PDDL

        if motion == 1:
            problem = 'mpir_pb1.pddl'
            filename = 'mpir_yes.txt'
            led_action = Planner(domain, problem, filename)
            print("LED_ON plan created")
            if str(led_action) == "(lighton human_yes pir_yes pir_yes)":
                print('led_on')
                print(led_action)
        
        elif motion ==0:
            problem = 'mpir_pb2.pddl'
            filename = 'mpir_no.txt'
            led_action = Planner(domain, problem, filename)
            print("LED_OFF plan created")
            if str(led_action) == "(lightoff human_no pir_no pir_no)":
                print('led_off')
                print(led_action)
            
    except KeyboardInterrupt:
        break