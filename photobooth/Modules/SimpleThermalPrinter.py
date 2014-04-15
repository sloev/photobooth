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

        args = [ "/dev/ttyAMA0", baudrate ]
        Serial.__init__(self, "/dev/ttyAMA0", baudrate)
        
        self.reset()
        self.setControlParameters()
        self.setDensity()
        self.setStatus()
        
    def reset(self):
        command=[27,64]
        self.writeBytes(command)
    def feed(self):
        command=[10]
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
        
        if width>384:
            width=384
        
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
        time.sleep(self.BYTE_TIME*len(command)) #four bytes in command
            
        self.writeBytes(data)
        time.sleep(self.BYTE_TIME*len(data))
            
    def writeBytes(self, bytes):
        for byte in bytes:
            char=chr(byte)
            super(SimpleThermalPrinter, self).write(char)
            time.sleep(self.BYTE_TIME)
          
def main():
    #
    printer=SimpleThermalPrinter()  
    data=[0]*384
    flip=True
    for i in range(384):
        data[i]=int(flip)
        flip=not flip
    for i in range(40):
        printer.printPixelLine(data)
    for i in range(2):
        printer.feed()
if __name__ == '__main__':
    main()

        
        


        