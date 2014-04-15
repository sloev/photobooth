'''
Created on Apr 15, 2014

@author: johannes
inspired by:
github.com/patriciogonzalezvivo/ofxThermalPrinter
and
Python library for the Adafruit Thermal Printer

'''
from serial import Serial
import time

class MyClass(Serial):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        baudrate = 19200

        args = [ "/dev/ttyAMA0", baudrate ]
        Serial.__init__(self, args)

        
                self.writeBytes(

        