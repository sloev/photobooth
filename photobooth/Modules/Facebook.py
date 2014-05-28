'''
Created on Mar 21, 2014

@author: johannes
'''
import json,time

from facepy import GraphAPI
from urlparse import parse_qs

import facepy

class Facebook(object):
    '''
    classdocs
    '''
    
    def __init__(self,config):
        try:
            token=facepy.utils.get_extended_access_token(config["token"],config['app_id'],config['app_secret']) 
            self.facebook = GraphAPI(token[0])
            print ("facebook token expires at "+str(token[1]))
            print ("token:"+str(token[0]))
        except:
            self.facebook=None
        
    def uploadImage(self,messageStr,imagePath):
        print("uploading to facebook")
        tries=0
        while(tries<5):
            try:
                self.facebook.post(
                                   path = 'Loppenbooth/photos',
                                   source = open(imagePath),
                                   message=messageStr
                                   )
                break
            except:
                print("facebook error, try #"+str(tries))
                time.sleep(0.1)
                tries=tries+1

        print("finnished uploading to facebook\n")


def main():
    import os
    with open('apiconfigs.txt', 'rb') as fp:
        config = json.load(fp)
        print("got config")
        facebook=Facebook(config["facebook"])
        facebook.uploadImage('lol hi lol',os.getcwd()+'/pics/IMG_0001.JPG')    

if __name__ == '__main__':
    main()