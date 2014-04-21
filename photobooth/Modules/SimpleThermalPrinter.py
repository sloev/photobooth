'''
Created on Apr 15, 2014

@author: johannes
inspired by:
github.com/patriciogonzalezvivo/ofxThermalPrinter
and
Python library for the Adafruit Thermal Printer

todo:
initialize density and setup

print line


'''
from serial import Serial
import time


class SimpleThermalPrinter(Serial):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        baudrate = 19200
        self.BYTE_TIME =(11.0) / float(baudrate)
        self.LINE_TIME=self.BYTE_TIME*10

        args = [ "/dev/ttyAMA0", baudrate ]
        Serial.__init__(self, "/dev/ttyAMA0", baudrate,timeout=1000)
        
        time.sleep(1)
        self.reset()
        time.sleep(1)
        
        #self.setControlParameters()
        #self.setDensity()
        #self.setStatus()
        #self.reverseFlip()
        #self.feed()
        
    def reset(self):
        command=[12]#flush
        self.writeLine(command)

        command=[27,64]
        self.writeLine(command)

    def feed(self,lines=1):
        command=[27,74,lines]
        self.writeLine(command)

#    def setControlParameters(self,heatingDots=60,  heatingTime=200, heatingInterval=250):
    def setControlParameters(self,heatingDots=7,  heatingTime=80, heatingInterval=2):
        command=[27,55,heatingDots,heatingTime,heatingInterval]
        self.writeBytes(command)
        command=[27, 51, 1]
        self.writeLine(command)
    
    def setDensity(self,printDensity=15, printBreakTime=15):
        command=[18,35,(printDensity << 4) | printBreakTime]
        self.writeLine(command)
        
    def setStatus(self,online=True):
        online=int(online)
        command=[37,62,online]
        self.writeLine(command)
     
    def writePixelLine(self,pixels):#always takes a list of 384 pixels
        width=len(pixels)
     #   if width>384:
      #      width=384
        data=[18,42,1,48]
        for i in range(0,width,8):
            byt=0
            for j in range(8):
                byt += pixels[i+j] << (7 - j)
            data.append(byt)
            
        self.writeLine(data)

    def writeLine(self, bytes):
        line=''.join(chr(b) for b in bytes)
        super(SimpleThermalPrinter, self).write(line)
        
    def resize(self,img):
        import Image,ImageOps
        width,height=img.size  
        if width>384:
            img=img.crop(((width/2)-(height/2),0,(width/2)+(height/2),height))
            img=img.resize((384,384))
            img=ImageOps.grayscale(img)
        return img
    
    def raster(self,image):
        import Image
        width,height=image.size

        img = image.convert('L')
        pixelArray=img.load()
        pixels=[0]*(width*height)

        threshold = 100*[0] + 156*[255]
        
        print "starting to dither"
        for y in range(height):
            for x in range(width):
        
                #old = img.getpixel((x, y))
                old=pixelArray[x,y]
                new = threshold[old]
                err = (old - new) >> 3 # divide by 8
                
                pixelArray[x,y]=new
                pixels[x+y*width]=new != 255

               # img.putpixel((x, y), new)
                nxy=(x+1,y)
                if nxy[0]<width:
                    pixels[nxy[0]+nxy[1]*width]=(pixelArray[nxy]+err)!=255

                    pixelArray[nxy]=pixelArray[nxy]+err

                    #img.putpixel(nxy,img.getpixel(nxy)+err)
                
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
                    
 
                '''
                        
                for nxy in [(x+1, y), (x+2, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x, y+2)]:
                    try:
                        img.putpixel(nxy, img.getpixel(nxy) + err)
                    except IndexError:
                        pass
                '''
        print "finnished dithering, putting image"
        #newim = Image.new("L",img.size)
        #newim.putdata(pixelArray)
        return [img,pixels]#.copy()
    
    def close(self):
        self.setStatus(False)
        super(SimpleThermalPrinter, self).flushOutput()
          
def main():
    #
    printer=SimpleThermalPrinter()  
    
    import sys,select,Image,ImageOps
    print "loading image"
    img=Image.open("test.jpg")
    print "resizing image"
    width,height=img.size

    img=img.crop(((width/2)-(height/2),0,(width/2)+(height/2),height))
    img=img.resize((384,384))
    img=ImageOps.grayscale(img)
    print "done"
    [img,tmptmp]=printer.raster(img)
    img.save("test2.jpg")
    
    print "s or d for lines"
    try:
        while True:
            time.sleep(1)
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                c = sys.stdin.readline()
                c=c[0:1]
                if(c=='s'): 
                    data=[]
                    counter=0
                    thresh=30
                    bol=False
                    for i in range(384*500):
                        tmp=0
                        counter+=1
                        if counter>thresh:
                            counter=0
                            bol=not bol
                        if bol:    
                            tmp=1
                        data.append(tmp)
                    for i in range(0,len(tmptmp),384):
                        
                        printer.writePixelLine(tmptmp[i:i+384])
                    printer.feed()
                    print "done - press s or d for lines"
                    
    except KeyboardInterrupt:
        print("exiting")
        pass
    printer.feed()
    
    printer.close()
if __name__ == '__main__':
    main()

        
        


        