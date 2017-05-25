#!/usr/bin/python -d

import sys
import math
import numpy
from PyQt4 import QtCore, QtGui
from PortDialog import Ui_PortDialog
from FeedbackViewer import Ui_ZeoViewer
from ZeoRawData import BaseLink, Parser
from matplotlib.lines import *
#from lucidCUE import *

class ZeoViewer(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        self.sampleLength = 128
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ZeoViewer()
        self.ui.setupUi(self)
        self.wave = [0]*self.sampleLength*2
        self.prevBadSignal = False #Used to determine color of previous seconds waveform
        self.hyp = []
        self.med = []
        self.old = []
        self.base = []
        self.hypToHeight = {'-2' : 0,
                            '-1' : 1,
                            '0'  : 2,
                            '+1' : 3,
                            '+2' : 4}
        #Colors grabbed from website
        self.hypColors = ['#000000', '#00552a', '#99989b', '#29a639', '#d05827']
        #Create initial baselines
        self.WaveForm = self.ui.WaveGraph.axes.plot(range(self.sampleLength*2), self.wave, color = 'g')[0]
        self.FFTbars = self.ui.FreqGraph.axes.bar((0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5), [0]*7, 1)
        self.Sleepbars = self.ui.SleepGraph.axes.bar(range(15,300,30), [0]*10, 30, color = 'w')
        
    def updateWaveform(self, waveform):
        self.wave = self.wave[self.sampleLength:] + waveform
        self.WaveForm.set_ydata(self.wave)
        self.ui.WaveGraph.draw()
            
    
    def updateFFT(self, bins):
        for i,bar in enumerate(self.FFTbars):
            bar.set_height(bins[i]*100) # Scaled to be essentially percents
        self.ui.FreqGraph.draw()
    
    def updateMednogram(self, bins):
        t=2 #theta bin [4 - 8]
        g=7 #gamma band [30 - 50]
            
        if len(self.med) < 30:
            self.med.append(bins[g]*100)
            
        else: #calculate stage of meditation
            if len(self.old) == 30:
                stage='0'
                if numpy.median(self.old)>(numpy.median(self.med)*1.5): #compare the mean bin of this epoch to the previous
                    stage='-2'
                    
                if numpy.median(self.old)>numpy.median(self.med) and numpy.median(self.old)<(numpy.median(self.med)*1.5):
                    stage='-1'

                if numpy.median(self.old)<numpy.median(self.med) and (numpy.median(self.old)*1.5)>numpy.median(self.med):
                    stage='+1'

                if (numpy.median(self.old)*1.5)<numpy.median(self.med):
                    stage='+2'
                
                self.hyp.append(self.hypToHeight[stage])
                    
            else: #this is the first epoch, so save the baseline
                self.base = numpy.median(self.med)
                self.old = self.med
                self.hyp.append(2)
                stage='0'
                
            if len(self.hyp) == 10: #game over
                print 'game over'
                sys.exit()
               
            #update the graph
            self.Sleepbars[len(self.hyp)-1].set_height(self.hyp[len(self.hyp)-1])
            self.Sleepbars[len(self.hyp)-1].set_color(self.hypColors[self.hyp[len(self.hyp)-1]])
            self.ui.SleepGraph.draw()
            #update the variables
            self.old = self.med
            self.med = []
            self.med.append(bins[g]*100)
        
    
    def updateSlice(self, slice):
        self.ui.TimeLabel.setText(QtGui.QApplication.translate('ZeoViewer', 
                                        slice['ZeoTimestamp'], 
                                        None, QtGui.QApplication.UnicodeUTF8))
        self.ui.VersionLabel.setText(QtGui.QApplication.translate('ZeoViewer', 
                                        'Version: ' + str(slice['Version']), 
                                        None, QtGui.QApplication.UnicodeUTF8))
                                        
        if not slice['SQI'] == None:
            sqi = str(slice['SQI'])
        else:
            sqi = '--'
        self.ui.SQILabel.setText(QtGui.QApplication.translate('ZeoViewer', 
                                    'SQI: ' + sqi + ' (0-30)', 
                                    None, QtGui.QApplication.UnicodeUTF8))
                                        
        if not slice['Impedance'] == None:
            imp = str(int(slice['Impedance']))
        else:
            imp = '--'
        self.ui.ImpLabel.setText(QtGui.QApplication.translate('ZeoViewer', 
                                    'Impedance: ' + imp, 
                                    None, QtGui.QApplication.UnicodeUTF8))
               
        if slice['BadSignal']:
            for i,bar in enumerate(self.FFTbars):
                bar.set_color('r')
            self.WaveForm.set_color('r')
        else:
            for i,bar in enumerate(self.FFTbars):
                bar.set_color('b')
            self.WaveForm.set_color('g')
                                     
        if not slice['Waveform'] == []:
            self.updateWaveform(slice['Waveform'])
                
        if len(slice['FrequencyBins'].values()) == 7:
            f = slice['FrequencyBins']
            bins = [f['2-4'],f['4-8'],f['8-13'],f['11-14'],f['13-18'],f['18-21'],f['30-50']]
            self.updateFFT(bins)
            self.updateMednogram(bins)
            
        #if not slice['SleepStage'] == None:
            #self.updateHypnogram(slice['SleepStage'])
    
    def updateEvent(self, timestamp, version, event):
        self.ui.TimeLabel.setText(QtGui.QApplication.translate('ZeoViewer', 
                                        timestamp, 
                                        None, QtGui.QApplication.UnicodeUTF8))
        self.ui.VersionLabel.setText(QtGui.QApplication.translate('ZeoViewer',
                                        'Version: ' + str(version), 
                                        None, QtGui.QApplication.UnicodeUTF8))
        self.ui.EventLabel.setText(QtGui.QApplication.translate('ZeoViewer', 
                                        event, 
                                        None, QtGui.QApplication.UnicodeUTF8))
    
        
class PortDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_PortDialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.StartBtn, QtCore.SIGNAL('clicked()'), self.openViewer)
        
    def openViewer(self):
        # Initialize
        viewer = ZeoViewer()
        link = BaseLink.BaseLink(str(self.ui.PortsListBox.currentText()))
        parser = Parser.Parser()
        # Add callbacks
        link.addCallback(parser.update)
        parser.addEventCallback(viewer.updateEvent)
        parser.addSliceCallback(viewer.updateSlice)
        # Start Link
        link.start()
        self.close()
        viewer.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialog = PortDialog()  
    dialog.show()
    
    sys.exit(app.exec_())
