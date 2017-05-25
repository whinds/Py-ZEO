#!/usr/bin/python -d

import sys
import math
import numpy
from PyQt4 import QtCore, QtGui
from PortDialog import Ui_PortDialog
from JediViewer import Ui_ZeoViewer
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
        self.med=[]
        self.foc=[]
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
        self.FocusBar = self.ui.FocusBar.axes.bar((0.5), [0]*1, 1, color = 'r')
        self.RelaxBar = self.ui.RelaxBar.axes.bar((0.5), [0]*1, 1, color = 'w')
        self.RelaxGraph = self.ui.RelaxGraph.axes.bar((0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5), [0]*11, 1)
        self.FocusGraph = self.ui.FocusGraph.axes.bar((0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5), [0]*11, 1)
        
    def updateWaveform(self, waveform):
        self.wave = self.wave[self.sampleLength:] + waveform
        self.WaveForm.set_ydata(self.wave)
        self.ui.WaveGraph.draw()
            
    
    def updateFFT(self, bins):
        for i,bar in enumerate(self.FFTbars):
            bar.set_height(bins[i]*100) # Scaled to be essentially percents
            if i==0 or i==1:
                bar.set_color(self.hypColors[4])
            if i==4 or i==5:
                bar.set_color(self.hypColors[1])
            
        self.ui.FreqGraph.draw()
    
    def updateFocusBar(self, bins):
        d=1 #delta bin [1 - 4]
        t=2 #theta bin [4 - 8]
        a_low=4 #alpha (low) band [11 - 14]
        a_hi=5 #alpha (high) band [13 - 18]
        #g=7 #gamma band [30 - 50]
            
        #self.med.append(bins[t]/(bins[a_low]+bins[a_hi]))               
               
        #update the graph
        self.FocusBar[0].set_height(round(((bins[d]+bins[t])/(bins[a_low]+bins[a_hi]))*100))
        self.FocusBar[0].set_color(self.hypColors[4])
        self.ui.FocusBar.draw()
        
    def updateRelaxBar(self, bins):
        d=1 #delta bin [1 - 4]
        t=2 #theta bin [4 - 8]
        a_low=4 #alpha (low) band [11 - 14]
        a_hi=5 #alpha (high) band [13 - 18]
        #g=7 #gamma band [30 - 50]
            
        #self.med.append(bins[t]/(bins[a_low]+bins[a_hi]))               
               
        #update the graph
        self.RelaxBar[0].set_height(round(((bins[a_low]+bins[a_hi])/(bins[d]+bins[t])*100)))
        self.RelaxBar[0].set_color(self.hypColors[1])
        self.ui.RelaxBar.draw()
        
    def updateRelaxGraph(self, bins):
        
        a_low=4 #alpha (low) band [11 - 14]
        a_hi=5 #alpha (high) band [13 - 18]
        #g=7 #gamma band [30 - 50]
            
        self.med.append((bins[a_low]+bins[a_hi]))
        self.r_avg=numpy.median(self.med)
               
        #update the graph
        for i,bar in enumerate(self.RelaxGraph):
            if i==0:
                bar.set_height(round((self.r_avg)*100))
                bar.set_color(self.hypColors[2])
            if len(self.med) >= i and i!=0:
                bar.set_height(round((self.med[len(self.med)-i]/self.r_avg)*100))
                bar.set_color(self.hypColors[1])
        self.ui.RelaxGraph.draw()

    def updateFocusGraph(self, bins):
        
        a_low=1 #alpha (low) band [11 - 14]
        a_hi=2 #alpha (high) band [13 - 18]
        #g=7 #gamma band [30 - 50]
            
        self.foc.append((bins[a_low]+bins[a_hi]))
        self.r_avg=numpy.median(self.foc)
               
        #update the graph
        for i,bar in enumerate(self.FocusGraph):
            if i==0:
                bar.set_height(round((self.r_avg)*100))
                bar.set_color(self.hypColors[0])
            if len(self.foc) >= i and i!=0:
                bar.set_height(round((self.foc[len(self.foc)-i]/self.r_avg)*100))
                bar.set_color(self.hypColors[4])
        self.ui.FocusGraph.draw()
        
    
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
            if not slice['BadSignal']:
                self.updateFocusBar(bins)
                self.updateRelaxBar(bins)
                self.updateRelaxGraph(bins)
                self.updateFocusGraph(bins)
            
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
