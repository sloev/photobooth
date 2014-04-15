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
        
        self.setControlParameters()
        self.setDensity()
        self.setStatus()
        #self.reverseFlip()
        #self.feed()
        
    def reset(self):
        command=[12]#flush
        self.writeBytes(command)

        command=[27,64]
        self.writeBytes(command)

        
    def reverseFlip(self):
        command=[29,66,1]
        self.writeBytes(command)
        command=[29,66,0]
        self.writeBytes(command)
        
    def feed(self,lines=1):
        command=[27,74,lines]
        self.writeBytes(command)

#    def setControlParameters(self,heatingDots=60,  heatingTime=200, heatingInterval=250):
    def setControlParameters(self,heatingDots=7,  heatingTime=80, heatingInterval=2):
        command=[27,55,heatingDots,heatingTime,heatingInterval]
        self.writeBytes(command)
        command=[27, 51, 1]
        self.writeBytes(command)
    
    def setDensity(self,printDensity=15, printBreakTime=15):
        command=[18,35,(printDensity << 4) | printBreakTime]
        self.writeBytes(command)
        
    def setStatus(self,online=True):
        online=int(online)
        command=[37,62,online]
        self.writeBytes(command)
        
    def printPixelLine(self,pixels):#takes a list of booleans
        #width=len(pixels)
        
        #if width>384:
            #width=384
        
        #rowBytes=int((width+7)/8)
        
        rowBytesClipped=48
        
        if rowBytesClipped >= 48:
            rowBytesClipped=48
        chunk=255

        data=[0]*(rowBytesClipped*chunk)
        for t in range(rowBytesClipped*chunk):
            
        #for i in range(width):
            bit=0
            if pixels[t]:
                bit=1
            index=int(t/8)
            byte=bit<<(7 - t % 8)
            data[index]+=byte
            
        command=[18,42,chunk,rowBytesClipped]
        self.writeBytes(command)
        #time.sleep(self.BYTE_TIME*len(command)) #four bytes in command
            
        self.writeBytes(data)
        #time.sleep(self.BYTE_TIME*len(data))
            
    def writeBytes(self, bytes):
        for byte in bytes:
            char=chr(byte)
            super(SimpleThermalPrinter, self).write(char)
            time.sleep(self.BYTE_TIME)
        #time.sleep(self.LINE_TIME)
        
    def close(self):
        self.setStatus(False)
        super(SimpleThermalPrinter, self).flushOutput()
          
def main():
    #
    printer=SimpleThermalPrinter()  
    data1=[1]*(384*255)
    data2=[1]*(384*255)
    flip=True
    for i in range(384*255):
        data1[i]=int(flip)
        flip=not flip

    import sys,select
    print "s or d for lines"
    try:
        while True:
            time.sleep(1)
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                c = sys.stdin.readline()
                c=c[0:1]
                if(c=='d'): 
                    for i in range(1):
                        printer.printPixelLine(data2)
                        printer.feed()
                    print "done - press s or d for lines"
                if(c=='s'): 
                    for i in range(1):
                        printer.printPixelLine(data1)
                        printer.feed()
                    print "done - press s or d for lines"
    except KeyboardInterrupt:
        print("exiting")
        pass
    printer.feed()
    
    printer.close()
if __name__ == '__main__':
    main()

        
        


        