'''
Created on Mar 19, 2014

@author: johannes
'''
import ptp2
import subprocess
import os, datetime
import twython

class Camera(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.camera_address = ptp2.util.list_ptp_cameras()[0]
        self.current_dir=os.getcwd()
        self.script ="require('lptpgui').exec_luafile([[A/CHDK/SCRIPTS/loppen.lua]])"


    def captureReturnDir(self):
        camera = ptp2.CHDKCamera(self.camera_address)

        camera.execute_lua(self.script,block=True)
        camera._wait_for_script_return()
        camera.close()
        
        print("finnished shooting")
        mydir = os.path.join(self.current_dir, "pics/"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(mydir)
        os.chdir(mydir)
        subprocess.call(['ptpcam','-G'])
        os.chdir(self.current_dir)
        
        print("finnished downloading")
        subprocess.call(['ptpcam','-D'])
        print("finito")
        
        return mydir
    
def main():
    print("started")
    cam=Camera()
    cam.captureReturnDir()
    
if __name__ == '__main__':
    main()
    