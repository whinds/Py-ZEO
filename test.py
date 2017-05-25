
import time
from time import localtime,strftime
import sys
import os
import subprocess
var1=2
var2=2
print time.time()
x=[time.time()]
time.sleep(2)
x.append(time.time())
print x[1]-x[0]
print x
# LUCID CUE INFO
audio_file = '/Users/kronkite/Downloads/PrettyLights-TakingUpYourPreciousTime/04 Finally Moving.mp3'
if var1==1 and var2==2:
    return_code = subprocess.Popen(["afplay",audio_file,'-v','2.2'],shell=False)
    time.sleep(5)
    return_code = subprocess.Popen(["killall","afplay"])