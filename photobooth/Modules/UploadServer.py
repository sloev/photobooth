'''
Created on Apr 10, 2014

@author: johannes
'''
from Twitter import Twitter
from Facebook import Facebook
import json

class Uploader(object):
    '''
    classdocs
    
    todo:
    lav en webserver
    lav en directory crawler der minutvist tjekker om der er nye filer i outgoing, uploader dem til respektive sider og sletter dem
    evt lave en mutex til directory sådan at kun webserveren ELLER director crawler kan slette/uploade en fil
    '''


    def __init__(self):
        '''
        Constructor
        '''
        with open('apiconfigs.txt', 'rb') as fp:
            config = json.load(fp)
            self.twitter=Twitter(config["twitter"])
            self.facebook=Facebook(config["facebook"])
    
        
def main():
    pass
if __name__ == '__main__':
    main()
        