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
        self.resumeTime      =  0.0
        self.dotPrintTime    =  0.60
        self.dotFeedTime     =  0.30

        args = [ "/dev/ttyAMA0", baudrate ]
        Serial.__init__(self, "/dev/ttyAMA0", baudrate)
        
        time.sleep(1)
        self.reset()
        
        #self.setControlParameters()
        #self.setDensity()
        #self.setStatus()
        #self.reverseFlip()
        #self.feed()
        
    def reset(self):
        #self.timeoutWait()
        command=[12]#flush
        self.writeLine(command)
        time.sleep(0.5)

        command=[27,64]
        self.writeLine(command)
        #self.timeoutSet(48*self.dotPrintTime)
        time.sleep(0.5)


    def feed(self,lines=1):
        self.timeoutWait()

        command=[27,74,lines]
        self.writeLine(command)
        self.timeoutSet(self.dotFeedTime)

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
        if width>384:print "error:width>384"
        
        data=[18,42,1,48]
        for i in range(0,width,8):
            byt=0
            for j in range(8):
                byt += pixels[i+j] << (7 - j)
            data.append(byt)
            
        self.timeoutWait()
        
        self.writeLine(data)
        
        d=self.dotFeedTime
        self.timeoutSet(d)
   
    def printPixelArray(self,pixels):
        #self.reset()
        for u in range(3):
            for i in range(0,len(pixels),384):
                self.writePixelLine(pixels[i:i+384])
        print "printed an image, sleeping now"
        #self.feed()
        print "woke up"
        

    def writeLine(self, bytes):
        line=''.join(chr(b) for b in bytes)
        super(SimpleThermalPrinter, self).write(line)

        
    def close(self):
        self.setStatus(False)
        super(SimpleThermalPrinter, self).flushOutput()
        
    def timeoutSet(self, x):
        self.resumeTime = time.time() + x

    # Waits (if necessary) for the prior task to complete.
    def timeoutWait(self):
        #print "waiting"
        while (time.time() - self.resumeTime) < 0: pass#original was pass


          
def main():
    #
    printer=SimpleThermalPrinter()  
    
    import sys,select,Image,ImageOps
    from ImageProcessor import ImageProcessor
    im=ImageProcessor()
    print "loading image"
    img=Image.open("test.jpg")
    print "resizing image"
    img=im.resizeForPrinter(img)
    tmptmp=im.rasterForPrinter(img)
    
    print "s or d for lines"
    try:
        while True:
            time.sleep(1)
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                c = sys.stdin.readline()
                c=c[0:1]
                if(c=='s'): 
                    printer.printPixelArray(tmptmp)
                 
#                    for i in range(0,len(tmptmp),384):
                        
 #                       printer.writePixelLine(tmptmp[i:i+384])
  #                  printer.feed()
  
                    print "done - press s or d for lines"
                    
    except KeyboardInterrupt:
        print("exiting")
        pass
    printer.feed()
    
    printer.close()
if __name__ == '__main__':
    main()

        
        


        