'''
Created on Mar 19, 2014

@author: johannes
'''
import Image
import ImageFont, ImageDraw, ImageOps,ImageChops
import os,glob
from Twitter import Twitter
from Facebook import Facebook
import datetime
import socket
from qrcode import *

#import zlib

class ImageProcessor(object):
    '''
    classdocs
    '''

    
    def __init__(self):
        '''
        Constructor
        '''
        '''getting ip'''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        self.ip=s.getsockname()[0]
        print("ip is:"+str(self.ip))
        s.close()
        '''got ip'''
        
        self.outgoingPath=os.path.join(os.getcwd()+"/outgoing/")

        self.twitterLayout={
                            "photoDim":750,
                            "width":1600,
                            "overlay":Image.open(os.getcwd()+"/templates/twitterOverlay.png")
                            }
        self.facebookLayout={
                            "photoDim":800,
                            "width":1600,
                            "overlay":Image.open(os.getcwd()+"/templates/facebookOverlay.png")
                            }
        
    def composeForTwitter(self,imagedir):
        print("composing for twitter")
        strip = Image.new('RGB', (self.twitterLayout["width"], self.twitterLayout["photoDim"]), (0,0,0)) 
        count=0
        dim=self.twitterLayout["photoDim"]
        for inFile in glob.glob(os.path.join(imagedir, '*.JPG')):
            if count>1: break
            print("\t"+str(inFile))
            img=Image.open(inFile)
            posX=5
            if count>0:posX=855
            posY=dim/2
            bbox=img.getbbox()
            img=img.crop(((bbox[2]/2)-(bbox[3]/2),0,(bbox[2]/2)+(bbox[3]/2),bbox[3]))
            img=img.resize((dim-10,dim-10))
            #img = ImageOps.autocontrast(img, cutoff=2)
            img=ImageOps.grayscale(img)
            
            strip.paste(img,(posX,5))
            count=count+1
        overlay=self.twitterLayout["overlay"]
        strip.paste(overlay,None,overlay)
        #path=os.path.join(imagedir, 'twitterStrip.PNG')
        #path=self.saveImageToOutgoing(strip,"twitter")

        #dateString=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        #path=os.path.join(self.outgoingPath,dateString+'_twitter.PNG')
        #strip.save(path, 'PNG')
        print("\n")
        return [strip,"twitter"]
    
    def composeForFacebook(self,imageDir):
        print("composing for facebook")
        strip = Image.new('RGB', (self.facebookLayout["width"], self.facebookLayout["width"]), (0,0,0)) 
        count=0
        dim=self.facebookLayout["photoDim"]
        positions={0:[5,5],1:[dim,5],2:[5,dim],3:[dim,dim]}
        for inFile in glob.glob(os.path.join(imageDir, '*.JPG')):
            if count>3:break
            print("\t"+str(inFile))
            img=Image.open(inFile)
            
            posX,posY=positions[count]
            bbox=img.getbbox()
            img=img.crop(((bbox[2]/2)-(bbox[3]/2),0,(bbox[2]/2)+(bbox[3]/2),bbox[3]))
            img=img.resize((dim-10,dim-10))
            #img = ImageOps.autocontrast(img, cutoff=2)
            img=ImageOps.grayscale(img)
            strip.paste(img,(posX,posY))
            count=count+1        
        overlay=self.facebookLayout["overlay"]
        strip.paste(overlay,None,overlay)
        #path=os.path.join(imageDir, 'facebookStrip.PNG')
        #path=self.saveImageToOutgoing(strip,"facebook")
        #dateString=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        #path=os.path.join(self.outgoingPath,dateString+'_facebook.PNG')
        #strip.save(path, 'PNG')
        print("\n")
        return [strip,"facebook"]
        #return path
    
    def saveImageToOutgoing(self,dateString,imageServicenameArray):
        #dateString=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        '''making a token for later deletion of image before upload'''

        tokenString="http://"+self.ip+":8080?stringToken="+dateString.encode('base64')
        qr = QRCode(version=10, error_correction=ERROR_CORRECT_L)
        qr.add_data(tokenString)
        qr.make() # Generate the QRCode itself

        # im contains a PIL.Image.Image object
        im = qr.make_image()

        for pairs in imageServicenameArray:
            image=pairs[0]
            serviceName=pairs[1]
            path=os.path.join(self.outgoingPath,dateString+'_'+serviceName)
            pathPNG=path+".PNG"
            pathDone=path+".done"
            pathQr=path+".qr.png"
            #pathDone=os.path.join(self.outgoingPath,dateString+'_'+serviceName+'.done')#used as kind of atomic stuff
            image.save(pathPNG, 'PNG')
            with open(pathDone, 'w') as doneFile:
                doneFile.write('done')
            # To save it
            im.save(pathQr)


        
        print "token is dateString:"+dateString+"\nencoded to:"+tokenString
        return tokenString

    def composeForPrinter(self,imageDir):
        print("composing For Printer")
        paths=["","",""]
        return paths
    
def main():
    import os
    print("started")
    message="Testing "+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    ip=ImageProcessor()
    facebookImageAndString=ip.composeForFacebook(os.getcwd()+"/pics")
    twitterImageAndString=ip.composeForTwitter(os.getcwd()+"/pics")
    
    dateString=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    
    token=ip.saveImageToOutgoing(
                           dateString,
                           [
                            facebookImageAndString,
                            twitterImageAndString
                            ])
    with open('apiconfigs.txt', 'rb') as fp:
        import json
        config = json.load(fp)
        #twitter=Twitter(config["twitter"])
        #twitter.uploadImage(message,twitterPath)
        #facebook=Facebook(config["facebook"])
        #facebook.uploadImage(message, facebookPath)
        
    ip.composeForPrinter(os.getcwd())
    
if __name__ == '__main__':
    main()