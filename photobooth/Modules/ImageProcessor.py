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
    
    def saveImageToOutgoing(self,dateString,imageServicenameArray,qrdir):
        #dateString=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        '''making a token for later deletion of image before upload'''

        tokenString="http://"+self.ip+":8080?stringToken="+dateString.encode('base64')
        qr = QRCode(version=None, error_correction=ERROR_CORRECT_H,border=0)
        qr.add_data(tokenString)
        qr.make(fit=True) # Generate the QRCode itself

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
            path2=os.path.join(qrdir,"0.JPG")
            im.save(path2)
            im.save(pathQr)

        print "token is dateString:"+dateString+"\nencoded to:"+tokenString
        return tokenString

    def composeForPrinterReturnPixelArrays(self,imageDir,number):
        print("composing For Printer")

        strip = Image.new('RGB', (384,384*(number+1)), (255,255,255))

        count=0
        pixels=[]
        for inFile in sorted(glob.glob(os.path.join(imageDir, '*.JPG'))):
            '''change to amount of pictures including qr code'''
            if count>number:
                break
            print inFile
            img=Image.open(inFile)
            img=self.resizeForPrinter(img)

            #pixels+=[self.rasterForPrinter(img)]
            strip.paste(img,(0,count*384))
                

            count+=1
        strip=ImageOps.grayscale(strip)
        strip.save("strip.jpg")
        pixels+=[self.rasterForPrinter(strip)]
        return pixels

    def resizeForPrinter(self,img):
        width,height=img.size  
        if width>384:
            img=img.crop(((width/2)-(height/2),0,(width/2)+(height/2),height))
            img = ImageOps.expand(img,border=5,fill='white')
            img=img.resize((384,384))
        return img
    
    '''
    returns a pixel array with 1's or 0's
    '''
    def rasterForPrinter(self,image):
        
        #image.save("ditheredOld.jpg")

        width,height=image.size

        img = image.convert('L')
        pixelArray=img.load()
        pixels=[0]*(width*height)

        threshold = 100*[0] + 156*[255]
        
        print "starting to dither"
        for y in range(height):
            for x in range(width):
        
                old=pixelArray[x,y]
                new = threshold[old]
                err = (old - new) >> 3 # divide by 8
                
                pixelArray[x,y]=new
                pixels[x+y*width]=new != 255

                nxy=(x+1,y)
                if nxy[0]<width:
                    pixels[nxy[0]+nxy[1]*width]=(pixelArray[nxy]+err)!=255

                    pixelArray[nxy]=pixelArray[nxy]+err
                
                nxy=(x+2,y)
                if nxy[0]<width:
                    pixels[nxy[0]+nxy[1]*width]=(pixelArray[nxy]+err)!=255

                    pixelArray[nxy]=pixelArray[nxy]+err
                
                nxy=(x-1,y+1)
                if nxy[0]>-1 and nxy[1]<height:
                    pixels[nxy[0]+nxy[1]*width]=(pixelArray[nxy]+err)!=255

                    pixelArray[nxy]=pixelArray[nxy]+err
                
                nxy=(x,y+1)
                if nxy[1]<height:
                    pixels[nxy[0]+nxy[1]*width]=(pixelArray[nxy]+err)!=255

                    pixelArray[nxy]=pixelArray[nxy]+err
                
                nxy=(x+1,y+1)
                if nxy[0]<width and nxy[1]<height:
                    pixels[nxy[0]+nxy[1]*width]=(pixelArray[nxy]+err)!=255

                    pixelArray[nxy]=pixelArray[nxy]+err
                
                nxy=(x,y+2)
                if nxy[1]<height:
                    pixels[nxy[0]+nxy[1]*width]=(pixelArray[nxy]+err)!=255

                    pixelArray[nxy]=pixelArray[nxy]+err

        print "finnished dithering, putting image"
        #newim = Image.new("L",img.size)
        #image.save("dithered.jpg")
        #newim.putdata(pixelArray)
        return pixels
    
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