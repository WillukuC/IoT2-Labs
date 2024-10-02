#!/usr/bin/env python
import RPi.GPIO as GPIO
import ADC0832
import time

def init():
    ADC0832.setup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)

def loop():
    while True:
        res = ADC0832.getADC(0)
        vol = 3.3/255 * res
        isDark = 'dark'
        if vol > 1.65:
            GPIO.output(16, GPIO.LOW)
            print ('analog value: %03d  ||  voltage: %.2fV  ||  the room is bright' %>
        else:
            GPIO.output(16, GPIO.HIGH)
            print ('analog value: %03d  ||  voltage: %.2fV  ||  the room is dark' %(r>
        time.sleep(0.2)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        print ('The end !')
