import os,time,glob
print "hello world"

def tap(x,y):
    os.system("sendevent /dev/input/event0 3 53 %d;sendevent /dev/input/event0 3 54 %d;sendevent /dev/input/event0 3 48 5;sendevent /dev/input/event0 3 58 50;sendevent /dev/input/event0 0 2 0; sendevent /dev/input/event0 0 0 0" %(x,y))
    time.sleep(0.05)
    os.system("sendevent /dev/input/event0 0 2 0;sendevent /dev/input/event0 0 0 0;sendevent /dev/input/event0 0 2 0; sendevent /dev/input/event0 0 0 0")

def initInstagram():
    tap(130,520)
    time.sleep(3)
    directory='/sdcard/DCIM/Camera'
    os.chdir(directory)


def uploadPhoto():
    tap(550,880)
    time.sleep(3)
    tap(170,790)
    time.sleep(3)
    tap(600,600)
#    tap(200,200)
    time.sleep(3)
    tap(20,450)
 #   tap(500,480)
    time.sleep(4)
    tap(1000,60)
    time.sleep(8)
    tap(1000,60)
    time.sleep(12)
    tap(1000,60)
    time.sleep(5)

def deleteAllPhotos():
    files=glob.glob('*.jpg')
    for filename in files:
        os.unlink(filename)
        print "deleted%s" %str(filename)
def imageExist():
    print "is there images"
    files=glob.glob('*.jpg')
    print files
    print len(files)
    return len(files)

time.sleep(5)
initInstagram()
time.sleep(3)
while(True):
    if len(glob.glob('*.jpg'))>0:
        print "image found, sleeping 1 minute"
        time.sleep(30)
        print "uploading photos"
        uploadPhoto()
        print "upload done\nnow deleting"
        deleteAllPhotos()
        print "delete done , now sleeping 300seconds"
    else:
        print "no image"
    time.sleep(30)
    print "woke up"
