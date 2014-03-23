'''
Created on Mar 19, 2014

@author: johannes
'''
import Image
import ImageFont, ImageDraw, ImageOps,ImageChops
import os,glob
from Twitter import Twitter
from Facebook import Facebook

class ImageProcessor(object):
    '''
    classdocs
    '''

    
    def __init__(self):
        '''
        Constructor
        '''
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
        path=os.path.join(imagedir, 'twitterStrip.PNG')
        strip.save(path, 'PNG')
        print("\n")
        return path
    
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
        path=os.path.join(imageDir, 'facebookStrip.PNG')
        strip.save(path, 'PNG')
        print("\n")
        return path
    
    def composeForPrinter(self,imageDir):
        print("composing For Printer")
        paths=["","",""]
        return paths
    
def main():
    import os
    print("started")
    ip=ImageProcessor()
    facebookPath=ip.composeForFacebook(os.getcwd()+"/pics")
    twitterPath=ip.composeForTwitter(os.getcwd()+"/pics")

    with open('apiconfigs.txt', 'rb') as fp:
        import json
        config = json.load(fp)
        twitter=Twitter(config["twitter"])
        twitter.uploadImage(twitterPath)
        facebook=Facebook(config["facebook"])
        facebook.uploadImage("lol", facebookPath)
        
    ip.composeForPrinter(os.getcwd())
    
if __name__ == '__main__':
    main()