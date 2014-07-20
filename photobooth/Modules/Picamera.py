'''
Created on Apr 22, 2014

@author: johannes
'''

import picamera
from PIL import Image
import io
import time

import threading
import datetime,os,time

class Producer(threading.Thread):
    
    def __init__(self, e,q):
        super(Producer, self).__init__()
        print "Producer Started"
        self.q = q
        self.e=e
    
    def run(self):
        for x in range(3):
            print "making number:%d" ,x
            self.q.put(x)
            time.sleep(1)
            if self.e.is_set():
                break
        print "producer done"
        
        
        import io
import time
import picamera
from PIL import Image

# Create the in-memory stream
stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')
# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
image = Image.open(stream)

class Picamera(object):
    '''
    classdocs
    '''


    def __init__(self,quitEvent,cameraToRasterQueue):
        '''
        Constructor
        '''
        self.camera=picamera.PiCamera()
        self.camera.resolution=(800,600)
        #self.current_dir=os.getcwd()
        self.cameraToRasterQueue = cameraToRasterQueue
        self.quitEvent=quitEvent
        self.stream = io.BytesIO()
        time.sleep(2)
        self.captureThread=threading.Thread(target=self.captureFourImages())
        
    def isCaptureThreadRunning(self):
        return self.captureThread.isAlive()
        
    def captureFourImagesThreaded(self,intervalSeconds=1):
        self.captureThread=threading.Thread(target=self.captureFourImages(), args=(intervalSeconds,))
        self.captureThread.daemon=True
        self.captureThread.start()

    def captureFourImages(self,intervalSeconds=1):
        #mydir = os.path.join(self.current_dir, "pi3cs/"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        #os.makedirs(mydir)
        #os.chdir(mydir)
        images=[]
        
        for i in range(4):
            time.sleep(intervalSeconds)
#            filename=str(i+1)+"image.JPG"
            self.camera.capture(stream,format='jpeg')
            self.stream.seek(0)
            images=images+[Image.open(stream)]
            print "image put in queue"
            if not i%2: #only sending even number to queue
                self.cameraToRasterQueue.put(images[i])
            if self.quitEvent.is_set():
                break
        mydir = os.path.join(self.current_dir, "pics/"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        os.chdir(mydir)
        print("saving images")
        for i in range(images.size()):
            images[i].save(str(i)+".jpg")
