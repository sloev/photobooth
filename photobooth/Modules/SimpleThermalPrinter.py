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
        self.BYTE_TIME =11.0 / float(baudrate)

        args = [ "/dev/ttyAMA0", baudrate ]
        Serial.__init__(self, "/dev/ttyAMA0", baudrate)
        
        self.setControlParameters()
        self.setDensity()
        self.setStatus()
    
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
        
        if width>384:
            width=384
        
        rowBytes=int((width+7)/8)
        
        rowBytesClipped=rowBytes
        
        if rowBytesClipped >= 48:
            rowBytesClipped=48
        
        data=[]
        
        for i in range(width):
            bit=0
            if pixels[i]:
                bit=1
            index=int(i/8)
            byte=bit<<(7 - i % 8)
            data[index]+=bit
            
        command=[18,42,1,rowBytesClipped]
        self.writeBytes(command)
        time.sleep(self.BYTE_TIME*len(command)) #four bytes in command
            
        self.writeBytes(data)
        time.sleep(self.BYTE_TIME*len(data))
            
    def writeBytes(self, bytes):
        for byte in bytes:
            super(SimpleThermalPrinter, self).write(chr(byte))
            time.sleep(self.BYTE_TIME)
          
def main():
    printer=SimpleThermalPrinter()  
    data=[]
    flip=True
    for i in range(384):
        data[i]=int(flip)
        flip=not flip
    printer.printPixelLine(data)
    
if __name__ == '__main__':
    main()

        
        


        