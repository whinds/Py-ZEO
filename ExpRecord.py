# Experimentally Record Data

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

# from win32com.client import Dispatch

# User customizable variables

port = '/dev/tty.usbserial'

f = open('Darwin_dream', 'w')

class ExpData:

    def updateSlice(self, slice):
        if not slice['Waveform'] == []:
            wave = slice['Waveform']
            waveS = str(wave)[1:-1] #take the brackets off the end
            timestamp = slice['ZeoTimestamp']
            timeS = time.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
            timeS2=str(time.mktime(timeS))
            
            #save the data
            f.write("%s, %s\n" % (timeS2, waveS))
            

#def updateEvent(self, event):
    
if __name__ == "__main__":

# Initialize Serial Link

    link = BaseLink.BaseLink(port)

    parser = Parser.Parser()

    cue = ExpData()

    #time.sleep(20000) #why is this here?

# Add Callbacks and Start the Link

    link.addCallback(parser.update)

    parser.addSliceCallback(cue.updateSlice)
    
      #parser.addEventCallback(cue.updateEvent)

    link.start()

# Infinitely loop to allow the script to run continuously

    while(True):
    
        time.sleep(5) #why is this here?

                                       #end of program