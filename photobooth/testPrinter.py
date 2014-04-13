'''
Created on Apr 13, 2014

@author: johannes
'''
#!/usr/bin/python

from Modules.ThermalPrinter import Adafruit_Thermal
import Image
printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=20)

# Test inverse on & off
# Print the 135x135 pixel QR code in adaqrcode.py
printer.feed(1)
image=Image.open("morten.jpg")
printer.printImage(image, True)

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults