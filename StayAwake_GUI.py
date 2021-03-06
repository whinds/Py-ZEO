# Snooze Cue
#GUI LIBS
from matplotlib.lines import *
from PyQt4 import QtCore, QtGui
import BasicTerminalGUI
from ZeoViewer import Ui_ZeoViewer
# System Libraries
from multiprocessing import Process
import os
import subprocess

import time

from time import localtime,strftime

import sys

# Zeo Libraries

from ZeoRawData import BaseLink, Parser

from ZeoRawData.Utility import *

# ActiveHome Libraries (Windows COM)

#from win32com.client import Dispatch

# User customizable variables
port = '/dev/tty.usbserial' #ZEO port
###################################
alarm_time = '6:06:00' #military time <Hour:Minutes:Seconds>
SnoozeBuffer = 30 #minutes
drift_off_time = 1 #minutes
#convert to machine time code
date = localtime()
timeD = time.strftime("%m/%d/%Y",date)
full_alarmtime='%s %s' %(timeD,alarm_time)
timeS = time.strptime(full_alarmtime, "%m/%d/%Y %H:%M:%S")
AlarmTimeNum=time.mktime(timeS)
#################################
# ALARM CUE INFO
alarm_tune = '/Users/kronkite/Downloads/PrettyLights-TakingUpYourPreciousTime/04 Finally Moving.mp3'

wsoi = 'Light' #'wake' stage of interest

wake_num = 0 #initialize the consecutive-stage counter

con_wake = 7 #define how many consecutive stages needed

# LUCID CUE INFO
audio_file = '/Users/kronkite/Downloads/PrettyLights-TakingUpYourPreciousTime/04 Finally Moving.mp3'

soi = {'Undefined', 'Awake'} #define the 'stage of interest'
nsoi = {'REM', 'Light', 'Deep'} #other stages
stage_num = 0 #initialize the consecutive-stage counter

con_stage = 1 #define how many consecutive stages needed

cueISrunning = 0 #binary on off to keep track if cue is running

blinks = 9 #how many screen flashes for CUE

init_time=time.time();

class lucidCue:

    def updateSlice(self, slice):
        
        if not slice['SleepStage'] == None: #only update if stage can be classified
            timestamp = slice['ZeoTimestamp']
            timeS = time.strptime(timestamp, "%m/%d/%Y %H:%M:%S")
            time_num=time.mktime(timeS)

            self.updateCue(slice['SleepStage'])
    
    def updateCue(self, stage):
        global stage_num,wake_num,cueISrunning
        print stage, str(time.ctime())
        if not stage == soi:
            stage_num=0 #reset the stage counter
            if cueISrunning:
                return_code = subprocess.Popen(["killall","afplay"],shell=False)
                cueISrunning=0
                print 'Lucidity Cue Ended'
        if stage in soi:
            stage_num+=1
        if not stage == wsoi:
            wake_num=0 #reset the stage counter
        if stage == wsoi:
            wake_num+=1

    def sendCue(self):
        global cueISrunning
        t0=time.time()
        #PLAY AUDIO
        return_code = subprocess.Popen(["afplay",audio_file,'-v','.22'],shell=False)
        cueISrunning=1
        #return_code = subprocess.Popen(["afplay",'-t','5',audio_file])
        # killall -STOP afplay
        # killall -CONT afplay
        #FLASH SCREEN
        for i in range(1, blinks): #play the light cue 10 times?
            #initiate a flashing screen
            return_code = subprocess.Popen(["brightness", "1"],shell=False) #flash on
            time.sleep(1) #wait one second
            return_code = subprocess.Popen(["brightness", "0"],shell=False) #flash off
            time.sleep(1) #wait one second
        print time.time()-t0

    def sendAlarm(self):
        t0=time.time()
        #PLAY AUDIO
        return_code = subprocess.Popen(["afplay",alarm_tune,'-v','2.2'],shell=False)
    
        #FLASH SCREEN
        for i in range(1, blinks): #play the light cue 10 times?
            #initiate a flashing screen
            return_code = subprocess.Popen(["brightness", "1"],shell=False) #flash on
            time.sleep(1) #wait one second
            return_code = subprocess.Popen(["brightness", "0"],shell=False) #flash off
            time.sleep(1) #wait one second
        print time.time()-t0

if __name__ == "__main__":

# Initialize GUI viewer
    app = QtGui.QApplication(sys.argv)
    viewer = BasicTerminalGUI.ZeoViewer()
# Initialize Serial Link


    link = BaseLink.BaseLink(port)
    
    parser = Parser.Parser()
    
    cue = lucidCue()

# Add Callbacks and Start the Link

    link.addCallback(parser.update)
    
    parser.addSliceCallback(cue.updateSlice)
    parser.addSliceCallback(viewer.updateSliceG)
    parser.addEventCallback(viewer.updateEvent)

    viewer.show()
    link.start()
    
    
    
    print 'Stay Awake...'
    #time.sleep(drift_off_time*60) #wait before starting callbacks
    #print 'Lucidity check started...'
    print time.ctime()
#sys.exit(app.exec_())
#app.exec_()

while (True):
    #__name__ == "__main__"
        # Check for Awake
    if  stage_num == con_stage:
            print 'WAKE UP!'
            cue.sendCue()
            print time.ctime()
            time.sleep(1800)
        #stage_num=0 #reset the stage counter
            # Check for alarm time and preferred sleep stage
#time.sleep(5) #why is this here?


                                       #end of program