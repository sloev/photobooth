'''
Created on Aug 6, 2014

@author: johannes
'''
import RPi.GPIO as GPIO
import threading,time

class LedDriver(object):
    '''
    classdocs
    '''


    def __init__(self,pwmLed):
        self.pwmLed=pwmLed
        self.currentDutyCycle=0
        self.pwmThread=threading.Thread(target=self.fade, args=(0,))

    def fadeUp(self):
        self.pwmThread=threading.Thread(target=self.fade, args=(0,))
        self.pwmThread.daemon=True
        self.pwmThread.start()
    
    def fadeDown(self):
        self.pwmThread=threading.Thread(target=self.fade, args=(100,))
        self.pwmThread.daemon=True
        self.pwmThread.start()
                
    def fade(self,dutyCycle):
        for i in range(self.currentDutyCycle,dutyCycle):
            self.pwmLed.ChangeDutyCycle(i)
            time.sleep(0.2)
        self.currentDutyCycle=dutyCycle

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT) #set pin 21 to output

    p = GPIO.PWM(3,0.1)        #set the PWM on pin 21 to 50%

    p.start(0)    
    
    ledDriver=LedDriver(p)
    ledDriver.fadeUp()
    time.sleep(5)
    ledDriver.fadeDown()
    p.stop()
    GPIO.cleanup()




 
if __name__ == '__main__':
    main()

        
        