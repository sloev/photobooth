'''
Created on Mar 19, 2014

@author: johannes
'''
from Modules.Camera import Camera
from Modules.Twitter import Twitter
from Modules.Facebook import Facebook
from Modules.ImageProcessor import ImageProcessor
from Modules.SimpleThermalPrinter import SimpleThermalPrinter
from Modules.Picamera import Picamera
import json,time,threading, sys, select
import datetime
import RPi.GPIO as GPIO

class Photobooth(object):
    '''
    classdocs
    '''

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
        '''
        Constructor
        '''
        #config=dict()
        #with open('apiconfigs.txt', 'rb') as fp:
            #config = json.load(fp)
        #self.twitter=Twitter(config["twitter"])
        #self.facebook=Facebook(config["facebook"])
        self.imageProcessor=ImageProcessor()
        #self.printer=Printer()
        #self.uploader=UploadServer()
        self.picamera=Picamera()
        self.printer=SimpleThermalPrinter()
        
        '''state thread'''
        self.stateThread=threading.Thread()

    def startShoot(self):
        if(not self.stateThread.is_alive()):
            print("shooting")
            self.stateThread=threading.Thread(target=self.shoot())
            self.stateThread.daemon = True                
            self.stateThread.start()
        else:
            print("busy shooting")
        
    def stopShoot(self):
        self.stateThread.join()

    def shoot(self):
        dir=self.picamera.captureFourImages()

        facebookImageAndString=self.imageProcessor.composeForFacebook(dir)
        twitterImageAndString=self.imageProcessor.composeForTwitter(dir)
        
        dateString=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        
        token=self.imageProcessor.saveImageToOutgoing(
                           dateString,
                           [
                            facebookImageAndString,
                            twitterImageAndString
                            ],dir)
        pixels=self.imageProcessor.composeForPrinterReturnPixelArrays(dir,2)
        for pixelarray in pixels:
            self.printer.printPixelArray(pixelarray)
        
        
        '''chdk shooting and downloading'''
        #photoDir=self.camera.captureReturnDir()
        #message="Testing "+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        '''make photoframe'''
        
        '''upload two first images to twitter'''
        #imagePath=self.image_processor.composeForTwitter(photoDir)
        #self.twitter.uploadImage(message,imagePath)
        
        #imagePath=self.image_processor.composeForFacebook(photoDir)
        #self.facebook.uploadImage(message,imagePath)
        
        '''make photostrip'''
       # image_paths=self.image_processor.composeForPrinter(photoDir)
        
        '''print photos'''
        #self.printer.printPhotoStrip(image_paths)
        print "press s to shoot"

        
def main():
    photobooth=Photobooth()
    print("press s to shoot")
    
    try:
        while True:
            time.sleep(1)
            if(GPIO.input(4)==0):
                time.sleep(0.1)
                if(GPIO.input(4)==0):
                    photobooth.startShoot()
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                c = sys.stdin.readline()
                c=c[0:1]
                if(c=='s'): 
                    photobooth.startShoot()
    except KeyboardInterrupt:
        print("exiting")
        photobooth.stopShoot()

if __name__ == '__main__':
    main()