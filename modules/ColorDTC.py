#!/usr/bin/python
from picamera.array import PiRGBArray
from matplotlib import pyplot as plt
from picamera import PiCamera
import DynamicObjectV2
import numpy as np
import webcolors
import os.path
import time
import cv2
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
Obj = DynamicObjectV2.Class

widths = 440
heigths = 280

resX = 6
resY = 6
count = 0
imc = 0

hue = 0
sat = 0
val = 0
camera = PiCamera()
camera.resolution = (widths, heigths)
camera.framerate = 32
camera.hflip = True

rawCapture = PiRGBArray(camera, size=(widths, heigths))

time.sleep(0.1)
##def closest_colour(requested_colour):
##    min_colours = {}
##    for key, name in webcolors.css3_hex_to_names.items():
##        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
##        rd = (r_c - requested_colour[0]) ** 2
##        gd = (g_c - requested_colour[1]) ** 2
##        bd = (b_c - requested_colour[2]) ** 2
##        min_colours[(rd + gd + bd)] = name
##    return min_colours[min(min_colours.keys())]

def dec_conv(x):
    return format(x, '03d')

def init(self):
    # put your self.registerOutput here
    self.registerOutput("colourDTC", Obj("R",0,"G",0,"B",0,"NewColor",True,"Working", False))

def run (self):
    # put your init and global variables here
    
    # main loop
    while 1:
        oldRGB = [0,0,0]
        newRGB = [0,0,0]
            # capture frames from the camera
        for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # This is used to store the index of the largest face found
                # This is considered in later code to be the face of interest
                #largestFaceIdx = -1
                
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                frame = image.array
                size = 20
                mag = 0.5
                x = (widths/2)- size
                y = (heigths/2) - size
                w = (widths/2) + size
                h = (heigths/2) + size

                
                # This block grabs an image from the camera and prepares
                # a grey version to be used in the face detection.
                #(ret,frame) = cam.read()
                
    ##            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                blr = cv2.blur(frame,(10,10))
                cv2.rectangle(frame,(x,y),(w,h),(255,0,0),1)
                cv2.line(frame, (x,y),(w,h),(255,0,0),1)
                cv2.line(frame, (x,h),(w,y),(255,0,0),1)
                cv2.circle(frame, (220, 140),2,(0,255,0),2)
                
                maskd = np.zeros(blr.shape[:2], np.uint8)
                maskd[130:150, 210:230] = 255
                con = cv2.mean(blr,mask = maskd)
                Red = int(con[2])#dec_conv(int(con[2]))
                Gre = int(con[1])#dec_conv(int(con[1]))
                Blu = int(con[0])#dec_conv(int(con[0]))
                cv2.putText(frame,"Red=(%r)" % Red, (1,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                cv2.putText(frame,"Green=(%r)" % Gre, (widths/3,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                cv2.putText(frame,"Blue=(%r)" % Blu, (2*widths/3,20), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)

                newRGB = [Red,Gre,Blu]
                if(newRGB != oldRGB):
                    oldRGB = newRGB
##                    requested_colour = (Red, Gre, Blu)
                    self.output("colourDTC",Obj("R",None,"G",None,"B",None,"NewColour",False,"Working", True))
##                    closest_name = closest_colour(requested_colour)
##                    Hex = webcolors.name_to_hex(closest_name).encode('ascii','ignore')
##                    cv2.putText(frame,"Name=(%r)" % str(closest_name), (widths/3,40), cv2.FONT_HERSHEY_SIMPLEX, mag, (0,255,0), 2)
                    self.output("colourDTC",Obj("R",Red,"G",Gre,"B",Blu,"NewColour",True,"Working",True))
##                self.output("colourDTC",Obj("R",Red,"G",Gre,"B",Blu))
##                print "B=%d, G=%d, R=%d" %(con[0],con[1],con[2])


##                cv2.imshow('frame', frame)
                cv2.imwrite("save.png", frame)
                new = cv2.imread("save.png")
                cv2.imshow('frame', new)
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                
                # Check for keypresses
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print "Q Pressed"
                    break
                

        print "Quitting..."
        '''cam.release()'''
        break
        cv2.destroyAllWindows()
