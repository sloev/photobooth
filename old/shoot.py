#http://twigstechtips.blogspot.dk/2013/09/pythontwitter-posting-tweets-with-images.html
import ptp2
import time
import subprocess
import os, datetime
import twython
import glob


def captureAndDownload():
    #Get the camera address
    camera_address = ptp2.util.list_ptp_cameras()[0]
    camera = ptp2.CHDKCamera(camera_address)
    
    currentDir=os.getcwd()
    #Simple check to make sure we're talking with CHDK OK
    #print("CHDK Version: {0}".format(camera.get_chdk_version()))
    
    #This should execute the shoot command
    #script=["set_record(1)","shoot()","set_record(0)"]
    script ="require('lptpgui').exec_luafile([[A/CHDK/SCRIPTS/loppen.lua]])"
    camera.execute_lua(script,block=True)
    camera._wait_for_script_return()
    camera.close()
    
    print("finnished shooting")
    mydir = os.path.join(os.getcwd(), "pics/"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(mydir)
    os.chdir(mydir)
    subprocess.call(['ptpcam','-G'])
    os.chdir(currentDir)
    
    print("finnished downloading")
    subprocess.call(['ptpcam','-D'])
    print("finito")
    return mydir

def deleteOlderDirs():
	currentDir=os.getcwd()
	
def uploadToTwitter(dir):
	print("uploading to twitter")
	twitter = twython.Twython(
	    "get",
	    "from",
	    "config",
	    "file"
	)
	os.chdir(dir)
	for file in glob.glob("*.JPG"):
		f = open(os.path.join(dir, file), 'rb')
		twitter.update_status_with_media(
		  status = "Testing"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
		  media = f
		)
	print("finnished tweating")
	#twitter.update_status(status = "Testing ")

dir = captureAndDownload()
uploadToTwitter(dir)
