#!/usr/bin/python
import DynamicObjectV2
import webcolors
import os.path
import serial
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
Obj = DynamicObjectV2.Class

ser = serial.Serial("/dev/ttyUSB0",57600)
time.sleep(3)

# put your imports here

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def sendMSG(Red,Gre,Blu):
    requested_colour = (Red, Gre, Blu)
    closest_name = closest_colour(requested_colour)
    Hex = webcolors.name_to_hex(closest_name).encode('ascii','ignore')
##  HexV = ColrDTC.Hex
##  Hex = "%s" %HexV
##    self.message(Hex)
##    Hex = "#101010"
    inpu = Hex[1:]
    ser.write('%s' %(Hex[1:]))
##    ser.write('ff0000')
    time.sleep(1)
    return inpu

def facePosScale(a,b,c):    
    reX = int(round((a*2.125)))
    reY = int(round((b*2.742)))
    reZ = int(round(((c-50)*2.55)))
    reP = (reX,reY,reZ)
    return reP




def init(self):
    # put your self.registerOutput here
    self.registerOutput("NeoPixle", Obj("Send", False))

def run (self):

    # main loop
    while 1:
        # put your logic here
        x = 0
        color = (0,0,0)
        # you can use: output, getInputs, message
        ColrDTC = self.getInputs().colourDTC
        HeadP = self.getInputs().facePos
        FaceD = self.getInputs().faceDet
##        self.message(ColrDTC.Working)
        if(ColrDTC.Working == True):
            sendMSG(ColrDTC.R, ColrDTC.G, ColrDTC.B)
        elif(FaceD.Face == True):
            color = facePosScale(HeadP.x,HeadP.y,HeadP.z)
            
            x = sendMSG(color[0], color[1], color[2])
##            x = sendMSG(1, 1, 1)

            self.message(x)

        # if you want to limit framerate, put it at the end
        time.sleep(0.1)


