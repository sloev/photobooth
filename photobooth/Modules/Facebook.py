'''
Created on Mar 21, 2014

@author: johannes
'''
import json

from facepy import GraphAPI
from urlparse import parse_qs

import facepy

class Facebook(object):
    '''
    classdocs
    '''
    
    def __init__(self,config):
  
        token=facepy.utils.get_extended_access_token(config["token"],config['app_id'],config['app_secret']) 
        self.facebook = GraphAPI(token[0])
        print ("facebook token expires at "+str(token[1]))
        print ("token:"+str(token[0]))
        

    def uploadImage(self,messageStr,imagePath):
        print("uploading to facebook")
        self.facebook.post(
            path = 'Loppenbooth/photobooth',
            source = open(imagePath),
            message=messageStr
        )
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