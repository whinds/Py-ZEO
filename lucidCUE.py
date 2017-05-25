# lucidLampCue

# System Libraries
import subprocess

import time

from time import localtime,strftime

import sys

#import winsound

#import pythoncom

# Zeo Libraries

from ZeoRawData import BaseLink, Parser

from ZeoRawData.Utility import *

# ActiveHome Libraries (Windows COM)

#from win32com.client import Dispatch

# User customizable variables
#audio_file = "/User/walterhinds/Desktop/ZEO/audio.wav"
audio_file = '/Users/kronkite/Downloads/PrettyLights-TakingUpYourPreciousTime/04 Finally Moving.mp3'

port = '/dev/tty.usbserial'

stage_num = 0 #initialize the consecutive-stage counter

con_stage = 7 #define how many consecutive stages needed

soi = 'REM' #define the 'stage of interest'

blinks = 9 #how many screen flashes for CUE

class lucidCue:

    def updateSlice(self, slice):

        if not slice['SleepStage'] == None:

            self.updateCue(slice['SleepStage'])

    def updateCue(self, stage):
        global stage_num
        print stage, str(time.ctime())
        if not stage == soi:
            stage_num=0 #reset the stage counter
        if stage == soi:
            stage_num+=1

    def sendCue(self):
        t0=time.time()
        #PLAY AUDIO
        # return_code = subprocess.call(["afplay", audio_file])
        # killall -STOP afplay
        # killall -CONT afplay
        #FLASH SCREEN
        for i in range(1, blinks): #play the light cue 10 times?
            #initiate a flashing screen
            return_code = subprocess.call(["brightness", "1"]) #flash on
            time.sleep(1) #wait one second
            return_code = subprocess.call(["brightness", "0"]) #flash off
            time.sleep(1) #wait one second
        print time.time()-t0

if __name__ == "__main__":

# Initialize Serial Link
    return_code = subprocess.call(["afplay", audio_file])
    
    link = BaseLink.BaseLink(port)

    parser = Parser.Parser()

    cue = lucidCue()
    

# Add Callbacks and Start the Link

    link.addCallback(parser.update)

    parser.addSliceCallback(cue.updateSlice)

    link.start()

    # Wait a little bit before becoming lucid
    print 'Waiting to drift off...'
    time.sleep(2700) #wait 45 minutes before starting callbacks
    print 'Lucidity check started...'
    print time.ctime

# Infinitely loop to allow the lucidity check to run continuously

while(True):
    if  stage_num>= con_stage: #must be in stage for ~ 5 mins
        cue.sendCue()
        print time.ctime()
        stage_num=0 #reset the stage counter
        sys.exit()
#time.sleep(5) #why is this here?

                                       #end of program