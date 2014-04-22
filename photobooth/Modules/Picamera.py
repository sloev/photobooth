'''
Created on Apr 22, 2014

@author: johannes
'''

import picamera
import datetime,os,time

class Picamera(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.camera=picamera.PiCamera()
        self.current_dir=os.getcwd()

        
    def captureFourImages(self,intervalSeconds=2):
        mydir = os.path.join(self.current_dir, "pics/"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        os.chdir(mydir)
        
        for i in range(4):
            time.sleep(intervalSeconds)
            filename=str(i)+"image.jpg"
            self.camera.capture(filename)
        os.chdir(self.current_dir)

        