#!/bin/sh
cd /home/pi/photobooth/photobooth ; 
/home/pi/photobooth/photobooth/Photobooth.py > /var/log/photobooth.log 2> /var/log/photobooth.err
/home/pi/photobooth/photobooth/Modules/UploadServer.py > /var/log/photobooth.log 2> /var/log/photobooth.err
