(define (problem pb1) (:domain HVAC)

(:objects 
 human_yes human_no  -presence
 pir_yes pir_no  -pir_sensor
 AQ_good AQ_bad  -airquality
 aq_good aq_bad  -AQ_sensor
 temp_high temp_low -temperature
 t_high t_low -temp_sensor
)

(:init
    (isHumanpresent human_yes)
    (isHumanabsent human_no)
    (isPIRpresent pir_yes)
    (isPIRabsent pir_no)
    (isAQgood AQ_good)
    (isAQbad AQ_bad)
    (isAQSensgood aq_good)
    (isAQSensbad aq_bad)
    (isTempHigh temp_high)
    (isTempSensHigh t_high)
    (isTempLow temp_low)
    (isTempSensLow t_low)
)

(:goal (led_on pir_yes)
)
)