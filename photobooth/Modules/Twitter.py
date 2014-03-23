'''
Created on Mar 19, 2014

@author: johannes
'''
import twython,json,time

class Twitter():
    '''
    classdocs
    '''
    
    
    
    
    def __init__(self,config):
        '''
        Constructor
        '''
        self.twitter = twython.Twython(
            config["api_key"],
            config["api_secret"],
            config["access_token"],
            config["access_secret"]
            )        
        
    def uploadImage(self,messageStr,path):
        print("uploading to twitter")
        f = open(path, 'rb')
        tries=0
        while(tries<5):
            try:
                self.twitter.update_status_with_media(
                                                      status = messageStr,
                                                      media = f
                                                      )
            except:
                print("twitter error, try #"+str(tries))
                time.sleep(500)
                tries=tries+1
        print("finnished tweating\n")

def main():
    print("started")
    with open('apiconfigs.txt', 'rb') as fp:
            config = json.load(fp)
            print("got config")
            twitter=Twitter(config["twitter"])
            twitter.uploadImage('test.JPG')

if __name__ == '__main__':
    main()