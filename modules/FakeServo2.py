#!/usr/bin/python

import time
import random

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import DynamicObjectV2
Obj = DynamicObjectV2.Class

# put your imports here

def init(self):
    # put your self.registerOutput here
    self.registerOutput("headPosition", Obj("x", 0, "y", 0))
    self.registerOutput("lampPosition", Obj("z",0))

def run (self):
    # put your init and global variables here
  
    # main loop
    while 1:
        # put your logic here
        # you can use: output, getInputs, message, flags
        self.output("headPosition", Obj("x", random.randint(0, 10), "y", random.randint(0, 10)))
        self.output("lampPosition", Obj("z", random.randint(0, 10)))
        # if you want to limit framerate, put it at the end
        time.sleep(0.2)
