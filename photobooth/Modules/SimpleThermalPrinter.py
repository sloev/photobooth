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
        self.BYTE_TIME =(11.0*2) / float(baudrate)
        self.LINE_TIME=0.05

        args = [ "/dev/ttyAMA0", baudrate ]
        Serial.__init__(self, "/dev/ttyAMA0", baudrate,timeout=1000)
        
        time.sleep(1)
        #self.reset()
        time.sleep(1)
        
        self.setControlParameters()
        self.setDensity()
        self.setStatus()
        self.feed()
        
    def reset(self):
        command=[27,64]
        self.writeBytes(command)
        
    def feed(self,lines=1):
        command=[27,74,lines]
        self.writeBytes(command)

    def setControlParameters(self,heatingDots=20,  heatingTime=200, heatingInterval=250):
        command=[27,55,heatingDots,heatingTime,heatingInterval]
        self.writeBytes(command)
    
    def setDensity(self,printDensity=14, printBreakTime=4):
        command=[18,35,(printBreakTime << 5) | printDensity]
        self.writeBytes(command)
        
    def setStatus(self,online=True):
        online=int(online)
        command=[37,62,online]
        self.writeBytes(command)
        
    def printPixelLine(self,pixels):#takes a list of booleans
        width=len(pixels)
        
        if width>383:
            width=383
        
        rowBytes=int((width+7)/8)
        
        rowBytesClipped=rowBytes
        
        if rowBytesClipped >= 48:
            rowBytesClipped=48
        
        data=[0]*rowBytesClipped
        
        for i in range(width):
            bit=0
            if pixels[i]:
                bit=1
            index=int(i/8)
            byte=bit<<(7 - i % 8)
            data[index]+=byte
            
        command=[18,42,1,rowBytesClipped]
        self.writeBytes(command)
        #time.sleep(self.BYTE_TIME*len(command)) #four bytes in command
            
        self.writeBytes(data)
        #time.sleep(self.BYTE_TIME*len(data))
            
    def writeBytes(self, bytes):
        for byte in bytes:
            char=chr(byte)
            super(SimpleThermalPrinter, self).write(char)
            time.sleep(self.BYTE_TIME)
        time.sleep(self.LINE_TIME)
    def close(self):
        super(SimpleThermalPrinter, self).flushOutput()
          
def main():
    #
    printer=SimpleThermalPrinter()  
    data=[0]*384
    flip=True
    for i in range(384):
        data[i]=int(flip)
        flip=not flip

    import sys,select
    try:
        while True:
            time.sleep(1)
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                c = sys.stdin.readline()
                c=c[0:1]
                if(c=='s'): 
                    for i in range(40):
                        printer.printPixelLine(data)
    except KeyboardInterrupt:
        print("exiting")
        pass
    printer.feed()
    
    printer.close()
if __name__ == '__main__':
    main()

        
        


        