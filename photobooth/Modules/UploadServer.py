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

'''
todo:
make this class check for a .delete file and go directly to delete if it finds such a file
this .delete file is created by another process

'''

class UploadServer(object):
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
        
        self.scheduler=sched.scheduler(time.time,time.sleep)
        self.scheduler.enter(2,1,self.upload,())
        
        self.uploadThread = threading.Thread(target=self.scheduler.run)
        self.uploadThread.start()
        
    def upload(self):
        for targetFile in glob.glob(os.path.join(self.outgoingPath, '*.done')):
            #print targetFile

            fileName=os.path.basename(targetFile)
            print fileName
            fileTime=datetime.datetime.strptime(fileName[:16], '%Y-%m-%d_%H-%M') 
            print fileTime
            
            
            currentTime=datetime.datetime.now()
            currentTimeString=currentTime.strftime('%Y-%m-%d_%H:%M:%S.%f')
            
            delete=False
            if os.path.isfile(targetFile[:len(targetFile)-5]+".delete"):
                delete=True
            elif (currentTime - fileTime).total_seconds() > 100:
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
                delete=True
                #os.remove(targetFile[:len(targetFile)-5]+".PNG")
                #os.remove(targetFile)
            else:
                pass
            if delete:
                print "deleting"
                for targetFile in glob.glob(os.path.join(self.outgoingPath, fileName[:len(fileName)-5]+'.*')):
                    os.remove(targetFile)
                    print"- "+str(targetFile)
                    #os.remove(targetFile[:len(targetFile)-5]+".PNG")
                #os.remove(targetFile)
                print "done"

        self.scheduler.enter(5, 1, self.upload,())

                
    
    def stopAll(self):
        map(self.scheduler.cancel,self.scheduler.queue)
        self.uploadThread.join()
    
        
def main():
    up=UploadServer()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        up.stopAll()
        
if __name__ == '__main__':
    main()
        