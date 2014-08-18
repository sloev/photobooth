'''
Created on Apr 22, 2014

@author: johannes
'''

import picamera
import Image
import io
import time

import threading
import datetime,os,time


class Picamera(object):
    '''
    classdocs
    '''


    def __init__(self,quitEvent,cameraToRasterQueue,socialPreprocessorQueue,ledDriver):
        '''
        Constructor
        '''
        self.camera=picamera.PiCamera()
      #  self.camera.resolution=(800,600)
        self.current_dir=os.getcwd()
        self.cameraToRasterQueue = cameraToRasterQueue
        self.socialPreprocessorQueue=socialPreprocessorQueue
        
        self.quitEvent=quitEvent
        time.sleep(2)
        self.captureThread=threading.Thread()
        self.snippet=Image.open(os.getcwd()+"/templates/snippet.png")
        self.ledDriver=ledDriver

    def isCaptureThreadRunning(self):
        return self.captureThread.isAlive()
        
    def captureFourImagesThreaded(self,intervalSeconds=1):
        self.captureThread=threading.Thread(target=self.captureFourImages, args=(intervalSeconds,))
        #self.captureThread.daemon=True
        self.captureThread.start()
        self.ledDriver.fadeUp()

    def captureFourImages(self,intervalSeconds=1):
        print "inside camera capture"
        images=[]
        
        for i in range(4):
            print "making stream"
            stream = io.BytesIO()

            time.sleep(intervalSeconds)
#            filename=str(i+1)+"image.JPG"
            #self.camera.capture(stream,format='jpeg')
            self.camera.capture(stream, format='jpeg')
            stream.seek(0)
            images=images+[Image.open(stream)]
            print "image put in queue"
            if not i%2: #only sending even number to queue
                self.cameraToRasterQueue.put(images[i])
            if self.quitEvent.is_set():
                break
        self.cameraToRasterQueue.put(self.snippet)
        
        self.socialPreprocessorQueue.put(images)
        self.ledDriver.fadeDown()