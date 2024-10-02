#!/usr/bin/env python
import ADC0832
import time

def init():
    ADC0832.setup()

def loop():
    while True:
        res = ADC0832.getADC(0)
        vol = 3.3/255 * res
        isDark = 'dark'
        if vol > 1.65:
            print ('analog value: %03d  ||  voltage: %.2fV  ||  the room is bright' %(res, vol))
        else:
            print ('analog value: %03d  ||  voltage: %.2fV  ||  the room is dark' %(res, vol))
        time.sleep(0.2)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        print ('The end !')
