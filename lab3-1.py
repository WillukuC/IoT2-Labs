import ADC0832
import time
import math

def init():
    ADC0832.setup()

def loop():
  while True:
    res = ADC0832.getADC(0)
    Vr = 3.3 * float(res) / 255
    Rt = 10000 * Vr / (3.3 - Vr)
    temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
    Cel = temp - 273.15
    Fah = Cel * 1.8 + 32

    print ('Rt : %.2f  || C° : %.2f || F° : %.2f' %(Rt,Cel,Fah))
    time.sleep(0.2)

if __name__ == '__main__':
    init()
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        print ('The end !')
