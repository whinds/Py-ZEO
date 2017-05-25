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

f = open('Amelia', 'w')

audio_file = "/User/walterhinds/Desktop/ZEO/audio.wav"

port = '/dev/tty.usbserial'

stage_num = 0 #initialize the consecutive-stage counter

con_stage = 8 #define how many consecutive stages needed

soi = 'REM' #define the 'stage of interest'

blinks = 9 #how many screen flashes for CUE

class lucidCue:
    
    def updateWave(self, slice):
        
        if not slice['Waveform'] == []:
            wave = slice['Waveform']
            waveS = str(wave)[1:-1] #take the brackets off the end
            timestamp = slice['ZeoTimestamp']
            timeS = time.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
            timeS2=str(time.mktime(timeS))
            
            #save the data
            f.write("%s, %s\n" % (timeS2, waveS))

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

    link = BaseLink.BaseLink(port)

    parser = Parser.Parser()

    cue = lucidCue()
    

# Add Callbacks and Start the Link

    link.addCallback(parser.update)

    parser.addSliceCallback(cue.updateSlice)
    parser.addSliceCallback(cue.updateWave)

    link.start()

    # Wait a little bit before becoming lucid
    print 'Waiting to drift off...'
    time.sleep(7200) #wait 120 minutes before starting cue check
    print 'Lucidity check started...'
    print time.ctime

# Infinitely loop to allow the lucidity check to run continuously

while(True):
    if  stage_num>= con_stage: #must be in stage for ~ 5 mins
        cue.sendCue()
        print time.ctime()
        stage_num=-12 #reset the stage counter
#time.sleep(5) #why is this here?

                                       #end of program