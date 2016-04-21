#!/usr/bin/python

import signal, os, time
import kivy
import PIL
##import time

kivy.require('1.9.2') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image as kivyImage
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from PIL import Image

# Some variables
photoPath = "/home/pi/Desktop/latest/tvcs-master/photobooth/"
##photoName = time.strftime("%Y%m%d%H%M%S") + "_photobooth.jpg"
photoName =  "thumbnail.jpg"
photoResize = 512, 384

# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import DynamicObjectV2
Obj = DynamicObjectV2.Class

# put your imports here

class MyApp(App):
        # Display the latest thumbnail
        photo = kivyImage(source="/home/pi/Desktop/latest/tvcs-master/photobooth/thumbnail.jpg")
        

        def build(self):
                
                # Set up the layout
                photobox = GridLayout(cols=3, spacing=10, padding=10)

                # Create the UI objects (and bind them to callbacks, if necessary)
                photoButton = Button(text="Photo", size_hint=(.20, 1)) # Button: 20% width, 100% height
                photoButton.bind(on_press=photo_callback) # when pressed, trigger the photo_callback function
                Button3 = Button(text="Exit", size_hint=(.20, 1))
                Button3.bind(on_press=press_callback)
                colorButton = Button(text="Color", size_hint=(.20, 1))
                colorButton.bind(on_press=color_callback)
                
                # Periodically refresh the displayed photo using the callback function
                Clock.schedule_interval(self.callback, 1)

                # Add the UI elements to the layout
                photobox.add_widget(photoButton)
                photobox.add_widget(self.photo)
                photobox.add_widget(Button3)
                photobox.add_widget(colorButton)
                
                return photobox
            
        # Callback for thumbnail refresh
        def callback(self, instance):
        
                self.photo.reload()



appInst = MyApp()

# This callback will be bound to the button:

def press_callback(obj):
        if obj.text == 'Exit':
                appInst.tvcsSelf.message("EXIT KIVY")
                os.kill(os.getpid(), signal.SIGINT)

# Callback function for color button
def color_callback(obj):
        appInst.tvcsSelf.output("settings", Obj("face", False, "color", True))
        # Define filename with timestamp
##        photoName = time.strftime("%Y%m%d%H%M%S") + "_photobooth.jpg"
        photoName =  "thumbnail.jpg"
        # Take photo using "raspistill"
##        os.system("sudo raspistill -p '144,48,512,384' --vflip -w 1920 -h 1440 -o " + photoPath + photoName)
        # Resize the high res photo to create thumbnail
        Image.open(photoPath + photoName).resize(photoResize, Image.ANTIALIAS).save(photoPath + "thumbnail.jpg")
        
# Callback function for photo button
def photo_callback(obj):
        appInst.tvcsSelf.output("settings", Obj("face", True, "color", False))
        # Define filename with timestamp
##        photoName = time.strftime("%Y%m%d%H%M%S") + "_photobooth.jpg"
        photoName =  "thumbnail.jpg"
        # Take photo using "raspistill"
##        os.system("sudo raspistill -p '144,48,512,384' --vflip -w 1920 -h 1440 -o " + photoPath + photoName)
        # Resize the high res photo to create thumbnail
        Image.open(photoPath + photoName).resize(photoResize, Image.ANTIALIAS).save(photoPath + "thumbnail.jpg")


def init(self):
    # put your self.registerOutput here
    self.registerOutput("settings", Obj("face", False, "color", False))

    appInst.tvcsSelf = self
    
    appInst.run()


def run (self):
    pass
