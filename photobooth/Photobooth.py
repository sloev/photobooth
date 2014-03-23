'''
Created on Mar 19, 2014

@author: johannes
'''
from Modules.Camera import Camera
from Modules.Twitter import Twitter
from Modules.ImageProcessor import ImageProcessor
from Modules.Printer import Printer
import json,time,threading, sys, select


class Photobooth(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.camera=Camera()
        config=dict()
        with open('apiconfigs.txt', 'rb') as fp:
            config = json.load(fp)
        self.twitter=Twitter(config["twitter"])
        self.image_processor=ImageProcessor()
        self.printer=Printer()
        
        '''state thread'''
        self.stateThread=threading.Thread(target=self.shoot())

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
        '''chdk shooting and downloading'''
        photoDir=self.camera.captureReturnDir()
        
        '''make photoframe'''
        
        '''upload two first images to twitter'''
        imagePath=self.image_processor.composeForTwitter(photoDir)
        self.twitter.uploadImage(imagePath)
        
        imagePath=self.image_processor.composeForFacebook(photoDir)
        self.facebook.uploadImage(imagePath)
        
        '''make photostrip'''
       # image_paths=self.image_processor.composeForPrinter(photoDir)
        
        '''print photos'''
        #self.printer.printPhotoStrip(image_paths)
        
def main():
    photobooth=Photobooth()
    print("press s to shoot")
    
    try:
        while True:
            time.sleep(1)
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