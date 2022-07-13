(define (domain HVAC)

    (:requirements
        :strips
        :typing
        :negative-preconditions
    )
    
    (:types temperature -object
    temp_sensor -object
    airquality -object
    AQ_sensor -object
    presence -object
    pir_sensor -object
    )
    
    (:predicates
    (isTempHigh ?th -temperature)
    (isTempLow ?tl -temperature)
    (isTempSensHigh ?h -temp_sensor)
    (isTempSensLow ?l -temp_sensor)
    (off_fan1 ?oc -temp_sensor)
    (on_fan1 ?xc -temp_sensor)
    
    (isAQgood ?g -airquality)
    (isAQbad ?b -airquality)
    (isAQSensgood ?sg -AQ_sensor)
    (isAQSensbad ?sb -AQ_sensor)
    (off_fan2 ?fo -AQ_sensor)
    (on_fan2 ?fx -AQ_sensor)
    
    (isHumanpresent ?hh -presence)
    (isHumanabsent ?aa -presence)
    (isPIRpresent ?ph -pir_sensor)
    (isPIRabsent ?pa -pir_sensor)
    (led_on ?lo -pir_sensor)
    (led_off ?lx -pir_sensor)
    
    )
    
    (:action SwitchONfan1
        :parameters (?th -temperature ?xc ?h -temp_sensor)
        :precondition (and (isTempHigh ?th) (isTempSensHigh ?h))
        :effect (on_fan1 ?xc)
    )
    
    (:action SwitchOFFfan1
        :parameters (?tl -temperature ?oc ?l -temp_sensor)
        :precondition (and (isTempLow ?tl) (isTempSensLow ?l))
        :effect (off_fan1 ?oc)
    )
        
    (:action SwitchONfan2
        :parameters (?b -airquality ?fx ?sb -AQ_sensor)
        :precondition (and (isAQbad ?b) (isAQSensbad ?sb))
        :effect (on_fan2 ?fx)
    )
    
    (:action SwitchOFFfan2
        :parameters (?g -airquality ?fo ?sg -AQ_sensor)
        :precondition (and (isAQgood ?g) (isAQSensgood ?sg))
        :effect (off_fan2 ?fo)
    )
    
    (:action LightON
        :parameters (?hh -presence ?lo ?ph -pir_sensor)
        :precondition (and (isHumanpresent ?hh) (isPIRpresent ?ph))
        :effect (led_on ?lo)
    )
    
    (:action LightOFF
        :parameters (?aa -presence ?lx ?pa -pir_sensor)
        :precondition (and (isHumanabsent ?aa) (isPIRabsent ?pa))
        :effect (led_off ?lx)
    )
    
    
)