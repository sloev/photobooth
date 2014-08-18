'''
Created on Aug 6, 2014

@author: johannes
uses
https://github.com/sarfata/pi-blaster/

'''
import RPi.GPIO as GPIO
import threading
import time
import Queue

class LedDriver(object):

    def __init__(self,pwmLed,q1,q2):
        self.q1=q1
        self.q2=q2
        self.pwmLed=pwmLed
        
        self.ledPin=18
        self.pwmThread=threading.Thread(target=self.fade)

    def fadeUp(self):
        self.pwmThread=threading.Thread(target=self.fade,args=(0,))
        self.pwmThread.daemon=True
        self.pwmThread.start()

    def fadeDown(self):
        self.pwmThread=threading.Thread(target=self.fade,args=(1,))
        self.pwmThread.daemon=True
        self.pwmThread.start()
    
    def fade(self,direction):
        if direction:
            for i in range(100,-1,-1):
                self.pwmLed.ChangeDutyCycle(i)
                time.sleep(0.01)
            self.pwmLed.stop(0)
        else:
            self.pwmLed.start(0)
            for i in range(0,101,1):
                self.pwmLed.ChangeDutyCycle(i)
                time.sleep(0.01)

def main():
    print "does not work"
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(18,GPIO.OUT)
    
    pwmLed=GPIO.PWM(18,2000)
    q1=Queue.Queue()
    q1.put("")
    q2=Queue.Queue()
    q2.put("")
    ledDriver=LedDriver(pwmLed,q1,q2)
    ledDriver.fadeUp()
    time.sleep(10)
    tmp=q1.get()
    tmp=q2.get()
    print"removed objects"
    time.sleep(5)
    print "finnished"

if __name__ == '__main__':
    main()

        
        