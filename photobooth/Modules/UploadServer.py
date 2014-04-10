'''
Created on Apr 10, 2014

@author: johannes
'''
from Twitter import Twitter
from Facebook import Facebook
import json
import threading
import sched
import os
import time,datetime
import glob

class Uploader(object):
    '''
    classdocs
'''


    def __init__(self,config=None):
        '''
        Constructor
        '''
        if config==None:
            with open('apiconfigs.txt', 'rb') as fp:
                config = json.load(fp)
            
        self.twitter=Twitter(config["twitter"])
        self.facebook=Facebook(config["facebook"])
        
        self.twitterMessage=config["twitter"]["message"]
        self.facebookMessage=config["facebook"]["message"]
            
            
        self.outgoingPath=os.path.join(os.getcwd()+"/outgoing/")
        
        self.Event=threading.Event()
        self.Event.set()
        
        #self.CloseEvent=threading.Event()
        #self.CloseEvent.clear()
        self.scheduler=sched.scheduler(time.time,time.sleep)
        self.scheduler.enter(2,1,self.upload,())
        
        self.uploadThread = threading.Thread(target=self.scheduler.run)
        self.uploadThread.start()
        
    def upload(self):
        self.Event.wait(1)
        self.Event.clear()

        for targetFile in glob.glob(os.path.join(self.outgoingPath, '*.done')):
            #print targetFile
            currentTime=datetime.datetime.now()
            currentTimeString=currentTime.strftime('%Y-%m-%d_%H:%M:%S.%f')
            fileName=os.path.basename(targetFile)
            print fileName
            fileTime=datetime.datetime.strptime(fileName[:16], '%Y-%m-%d_%H-%M') 
            print fileTime
            if (currentTime - fileTime).total_seconds() > 20:
            #if fileTime < datetime.datetime.now()-datetime.timedelta(seconds=20):
                '''then upload'''
                serviceName=fileName[17:len(fileName)-5]
                if(serviceName=="twitter"):
                    print "twitter done file found \nnow uploading"
                    self.twitter.uploadImage(self.twitterMessage+" "+currentTimeString,targetFile[:len(targetFile)-5]+".PNG")
                    print "done"
                elif(serviceName=="facebook"):
                    print "facebook done file found\nnow uploading"
                    self.facebook.uploadImage(self.facebookMessage+" "+currentTimeString,targetFile[:len(targetFile)-5]+".PNG")
                    print "done"
                '''deleting'''
                print "deleting"
                os.remove(targetFile[:len(targetFile)-5]+".PNG")
                os.remove(targetFile)
                print "done"
            else:
                pass
        self.Event.set()
        self.scheduler.enter(20, 1, self.upload,())
    
    def stopAll(self):
        map(self.scheduler.cancel,self.scheduler.queue)
        self.uploadThread.join()
    
        
def main():
    up=Uploader()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        up.stopAll()
        
if __name__ == '__main__':
    main()
        