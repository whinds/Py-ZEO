# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PortDialog.ui'
#
# Created: Wed Jul 28 12:45:43 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from serial import *
from glob import glob

class Ui_PortDialog(object):
    def setupUi(self, PortDialog):
        PortDialog.setObjectName('PortDialog')
        PortDialog.resize(388, 110)
        self.verticalLayout = QtGui.QVBoxLayout(PortDialog)
        self.verticalLayout.setObjectName('verticalLayout')
        self.PortsBox = QtGui.QHBoxLayout()
        self.PortsBox.setObjectName('PortsBox')
        self.PortsListBox = QtGui.QComboBox(PortDialog)
        self.PortsListBox.setEditable(True)
        self.PortsListBox.setObjectName('PortsListBox')
        self.PortsBox.addWidget(self.PortsListBox)
        self.PortScanBtn = QtGui.QPushButton(PortDialog)
        self.PortScanBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.PortScanBtn.setObjectName('PortScanBtn')
        self.PortsBox.addWidget(self.PortScanBtn)
        self.verticalLayout.addLayout(self.PortsBox)
        self.ButtonBox = QtGui.QHBoxLayout()
        self.ButtonBox.setObjectName('ButtonBox')
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.ButtonBox.addItem(spacerItem)
        self.StartBtn = QtGui.QPushButton(PortDialog)
        self.StartBtn.setObjectName('StartBtn')
        self.ButtonBox.addWidget(self.StartBtn)
        self.CancelBtn = QtGui.QPushButton(PortDialog)
        self.CancelBtn.setObjectName('CancelBtn')
        self.ButtonBox.addWidget(self.CancelBtn)
        self.verticalLayout.addLayout(self.ButtonBox)

        self.retranslateUi(PortDialog)
        QtCore.QObject.connect(self.CancelBtn, QtCore.SIGNAL('clicked()'), PortDialog.close)
        QtCore.QObject.connect(self.PortScanBtn, QtCore.SIGNAL('clicked()'), self.scanPorts)
        QtCore.QMetaObject.connectSlotsByName(PortDialog)
        

    def retranslateUi(self, PortDialog):
        PortDialog.setWindowTitle(QtGui.QApplication.translate('PortDialog', 'Zeo Raw Data Viewer', None, QtGui.QApplication.UnicodeUTF8))
        self.PortScanBtn.setText(QtGui.QApplication.translate('PortDialog', 'Scan Ports', None, QtGui.QApplication.UnicodeUTF8))
        self.StartBtn.setText(QtGui.QApplication.translate('PortDialog', 'Start', None, QtGui.QApplication.UnicodeUTF8))
        self.CancelBtn.setText(QtGui.QApplication.translate('PortDialog', 'Cancel', None, QtGui.QApplication.UnicodeUTF8))
        PortDialog.setWindowIcon(QtGui.QIcon('zeo.png'))
        
    def scanPorts(self):
        self.PortsListBox.clear()
        # Helps find USB>Serial converters on linux
        for p in glob('/dev/tty.usbserial*'):
            self.PortsListBox.addItem(p)
        #Linux and Windows
        for i in range(256):
            try:
                ser = Serial(i)
                if ser.isOpen(): 
                    #Check that the port is actually valid
                    #Otherwise invalid /dev/ttyS* ports may be added
                    self.PortsListBox.addItem(ser.portstr)
                ser.close()
            except SerialException:
                pass
        
        
