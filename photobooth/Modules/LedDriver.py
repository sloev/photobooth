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
        self.pwmThread=threading.Thread(target=self.fade)
        self.pwmThread.daemon=True
        self.pwmThread.start()
    
    def fade(self):
        self.pwmLed.start(0)
        print "opening piblaster in thread"
        #blaster_file = open("/dev/pi-blaster", "a")
        for i in range(0,101,1):
            #blaster_file.write("%d=%f\n"%(self.ledPin,value))
            self.pwmLed.ChangeDutyCycle(i)
            time.sleep(0.01)
        #self.pwmLed.stop(100)
        print "faded up"
        time.sleep(10)#wait for camera to shoot one picture
        print "led going in wait loop"
        while((not self.q1.empty()) or (not self.q2.empty())):
            time.sleep(0.1)
        print "queues empty"
        time.sleep(4)
        #self.pwmLed.start(100)
        for i in range(100,-1,-1):
            self.pwmLed.ChangeDutyCycle(i)
            #blaster_file.write("%d=%f\n"%(self.ledPin,value))
            time.sleep(0.01)
        print "faded down"
      #  blaster_file.close()
        self.pwmLed.stop(0)


def main():
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

        
        