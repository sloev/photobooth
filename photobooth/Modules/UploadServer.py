'''
Created on Apr 10, 2014

@author: johannes
'''
from Twitter import Twitter
from Facebook import Facebook
import json
import threading
import sched
import time

class Uploader(object):
    '''
    classdocs
'''


    def __init__(self):
        '''
        Constructor
        '''
        #with open('apiconfigs.txt', 'rb') as fp:
            #config = json.load(fp)
            #self.twitter=Twitter(config["twitter"])
            #self.facebook=Facebook(config["facebook"])
            
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
        print "lol"
            

        self.Event.set()
        self.scheduler.enter(2, 1, self.upload,())
    
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
        