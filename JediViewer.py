
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtCore import QSize

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure

from matplotlib import rcParams
rcParams['font.size'] = 8

class Ui_ZeoViewer(object):
    def setupUi(self, ZeoViewer):
        ZeoViewer.setObjectName('ZeoViewer')
        ZeoViewer.resize(1400, 500)
        self.centralwidget = QtGui.QWidget(ZeoViewer)
        self.centralwidget.setObjectName('centralwidget')
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName('verticalLayout')
        
        self.TopBox = QtGui.QHBoxLayout()
        self.TopBox.setObjectName('TopBox')
        
        self.FocusBar = plotWidget(self.centralwidget)
        self.FocusBar.axes.set_title('Focus')
        self.FocusBar.axes.set_xlabel('(Theta + Delta)/Alpha')
        self.FocusBar.axes.set_ylabel('%')
        self.FocusBar.axes.set_position([0.2, 0.2, 0.7, 0.7])
        self.FocusBar.axes.set_yticks(range(0,201,10))
        self.FocusBar.axes.set_xticks(range(0,3,1))
        self.FocusBar.axes.set_xticklabels(('','',''))
        self.FocusBar.axes.get_xaxis().tick_bottom()
        self.FocusBar.axes.get_yaxis().tick_left()
        self.FocusBar.setObjectName('FocusBar')
        self.FocusBar.figure.set_facecolor('w')
        self.TopBox.addWidget(self.FocusBar)
        
        self.WaveGraph = plotWidget(self.centralwidget)
        self.WaveGraph.axes.set_title('Waveform')
        self.WaveGraph.axes.set_xlabel('Time (s)')
        self.WaveGraph.axes.set_ylabel('Voltage (uV)')
        self.WaveGraph.axes.set_position([0.08, 0.2, 0.84, 0.6])
        self.WaveGraph.axes.set_xticks(range(0,257,128))
        self.WaveGraph.axes.set_xticklabels(('0','1', '2'))
        self.WaveGraph.axes.set_yticks(range(-150,151, 50))
        self.WaveGraph.axes.get_xaxis().tick_bottom()
        self.WaveGraph.axes.get_yaxis().tick_left()
        self.WaveGraph.setObjectName('WaveGraph')
        self.WaveGraph.figure.set_facecolor('w')
        self.TopBox.addWidget(self.WaveGraph)
        
        self.RelaxBar = plotWidget(self.centralwidget)
        self.RelaxBar.axes.set_title('Relaxation')
        self.RelaxBar.axes.set_xlabel('Alpha/(Delta+Theta)')
        self.RelaxBar.axes.set_ylabel('%')
        self.RelaxBar.axes.set_position([0.2, 0.2, 0.7, 0.7])
        self.RelaxBar.axes.set_yticks(range(0,201,10))
        self.RelaxBar.axes.set_xticklabels(('','',''))
        self.RelaxBar.axes.set_xticks(range(0,3,1))
        self.RelaxBar.axes.get_xaxis().tick_bottom()
        self.RelaxBar.axes.get_yaxis().tick_left()
        self.RelaxBar.setObjectName('RelaxBar')
        self.RelaxBar.figure.set_facecolor('w')
        self.TopBox.addWidget(self.RelaxBar)
        
        self.verticalLayout.addLayout(self.TopBox)
        
        self.ResultBox = QtGui.QHBoxLayout()
        self.ResultBox.setObjectName('ResultBox')
        
        self.FocusGraph = plotWidget(self.centralwidget)
        self.FocusGraph.axes.set_title('Focus Meter')
        self.FocusGraph.axes.set_xlabel('Time (s)')
        self.FocusGraph.axes.set_ylabel('% of running avg.')
        self.FocusGraph.axes.set_position([0.2, 0.2, 0.7, 0.7])
        self.FocusGraph.axes.set_yticks(range(0,160,10))
        self.FocusGraph.axes.set_xticks(range(13))
        self.FocusGraph.axes.set_xticklabels(('','Avg.', '0', '-1', '-2', '-3','-4','-5','-6','-7','-8','-9'))
        self.FocusGraph.axes.get_xaxis().tick_bottom()
        self.FocusGraph.axes.get_yaxis().tick_left()
        self.FocusGraph.setObjectName('FocusGraph')
        self.FocusGraph.figure.set_facecolor('w')
        self.ResultBox.addWidget(self.FocusGraph)
        
        self.FreqGraph = plotWidget(self.centralwidget)
        self.FreqGraph.axes.set_title('FFT')
        self.FreqGraph.axes.set_xlabel('Frequency Bins (Hz)')
        self.FreqGraph.axes.set_ylabel('Relative Power (%)')
        self.FreqGraph.axes.set_xticks(range(9))
        self.FreqGraph.axes.set_xticklabels(('','2-4', '4-8', '8-13', '11-14', '13-18', '18-21', '30-50'))
        self.FreqGraph.axes.set_yticks(range(0,101,10))
        self.FreqGraph.axes.get_xaxis().tick_bottom()
        self.FreqGraph.axes.get_yaxis().tick_left()
        self.FreqGraph.figure.autofmt_xdate()
        self.FreqGraph.axes.set_position([0.15, 0.25, 0.75, 0.65])
        self.FreqGraph.setObjectName('FreqGraph')
        self.FreqGraph.figure.set_facecolor('w')
        self.ResultBox.addWidget(self.FreqGraph)
        
        self.RelaxGraph = plotWidget(self.centralwidget)
        self.RelaxGraph.axes.set_title('Relax Meter')
        self.RelaxGraph.axes.set_xlabel('Time (s)')
        self.RelaxGraph.axes.set_ylabel('% of running avg.')
        self.RelaxGraph.axes.set_position([0.2, 0.2, 0.7, 0.7])
        self.RelaxGraph.axes.set_yticks(range(0,160,10))
        self.RelaxGraph.axes.set_xticks(range(13))
        self.RelaxGraph.axes.set_xticklabels(('','Avg.', '0', '-1', '-2', '-3','-4','-5','-6','-7','-8','-9'))
        self.RelaxGraph.axes.get_xaxis().tick_bottom()
        self.RelaxGraph.axes.get_yaxis().tick_left()
        self.RelaxGraph.setObjectName('RelaxGraph')
        self.RelaxGraph.figure.set_facecolor('w')
        self.ResultBox.addWidget(self.RelaxGraph)
        
        self.verticalLayout.addLayout(self.ResultBox)
        self.StatusBox = QtGui.QHBoxLayout()
        self.StatusBox.setObjectName('StatusBox')
        
        self.TimeLabel = QtGui.QLabel(self.centralwidget)
        self.TimeLabel.setObjectName('TimeLabel')
        self.StatusBox.addWidget(self.TimeLabel)
        
        self.VersionLabel = QtGui.QLabel(self.centralwidget)
        self.VersionLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.VersionLabel.setObjectName('VersionLabel')
        self.StatusBox.addWidget(self.VersionLabel)
        
        self.SQILabel = QtGui.QLabel(self.centralwidget)
        self.SQILabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SQILabel.setObjectName('SQILabel')
        self.StatusBox.addWidget(self.SQILabel)
        
        self.ImpLabel = QtGui.QLabel(self.centralwidget)
        self.ImpLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ImpLabel.setObjectName('ImpLabel')
        self.StatusBox.addWidget(self.ImpLabel)
        
        self.EventLabel = QtGui.QLabel(self.centralwidget)
        self.EventLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.EventLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EventLabel.setObjectName('EventLabel')
        self.StatusBox.addWidget(self.EventLabel)
        
        self.verticalLayout.addLayout(self.StatusBox)
        ZeoViewer.setCentralWidget(self.centralwidget)

        self.retranslateUi(ZeoViewer)
        QtCore.QMetaObject.connectSlotsByName(ZeoViewer)

    def retranslateUi(self, ZeoViewer):
        ZeoViewer.setWindowTitle(QtGui.QApplication.translate('ZeoViewer', 'Zeo Raw Data Viewer', None, QtGui.QApplication.UnicodeUTF8))
        self.TimeLabel.setText(QtGui.QApplication.translate('ZeoViewer', '--/--/---- --:--:--', None, QtGui.QApplication.UnicodeUTF8))
        self.VersionLabel.setText(QtGui.QApplication.translate('ZeoViewer', 'Version: --', None, QtGui.QApplication.UnicodeUTF8))
        self.SQILabel.setText(QtGui.QApplication.translate('ZeoViewer', 'SQI: -- (0-30)', None, QtGui.QApplication.UnicodeUTF8))
        self.ImpLabel.setText(QtGui.QApplication.translate('ZeoViewer', 'Impedance: --Kohms', None, QtGui.QApplication.UnicodeUTF8))
        self.EventLabel.setText(QtGui.QApplication.translate('ZeoViewer', 'NO EVENT', None, QtGui.QApplication.UnicodeUTF8))
        ZeoViewer.setWindowIcon(QtGui.QIcon('zeo.png'))
        
class plotWidget(Canvas):
    """
    Simplified graphing widget created based on:
        Copyright 2009 Pierre Raybaut
        This software is licensed under the terms of the MIT License

        Derived from 'embedding_in_pyqt4.py':
        Copyright 2005 Florent Rougon, 2006 Darren Dale
    """

    def __init__(self, parent=None, width=3, height=2):
        self.figure = Figure(figsize=(width, height), dpi=100)
        self.axes = self.figure.add_subplot(111, autoscale_on=False)
        self.axes.hold(True)

        Canvas.__init__(self, self.figure)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QSize(w, h)

    def minimumSizeHint(self):
        return QSize(10, 10)
