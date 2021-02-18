import sys

import serial
import time

from PyQt5.QtCore import pyqtSlot

from comPortSetup import getComportsList
from MainApplicationUI import MainApplicationWindow
from ArduinoCodeCopyBtn import CopyCodeBtn

from PyQt5 import QtWidgets, QtGui, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QLabel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCanvas
import matplotlib.pyplot as plt
import numpy as np


class ConnectWindow(QMainWindow):

    def __init__(self):

        super(ConnectWindow, self).__init__()

        self.w = 700
        self.h = 400

        self.comPortList = getComportsList()
        self.arduinoIsConnected = False

        self.ser = ser = serial.Serial(
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
        self.arduinoName = ""

        self.setGeometry(300, 200, self.w, self.h)
        self.setFixedSize(self.w, self.h)
        self.setWindowTitle("Open Source Lab | Optics - Connect")

        self.initUi()

    def initUi(self):

        self.cb = QtWidgets.QComboBox(self)
        for i in self.comPortList:
            self.cb.addItem("Name : " + str(i["name"]) + " (Manufacturer : " + str(i["manufacturer"]) + ")",
                            i["device"])
        self.cb.adjustSize()
        self.cb.setMinimumWidth(self.cb.width() + 15)
        self.cb.move(int((self.w / 2) - (self.cb.width() / 2)), int((self.h / 2) - (self.cb.height() / 2)))

        self.selectLabel = QtWidgets.QLabel(self)
        self.selectLabel.setText("Select Arduino Com Port")
        self.selectLabel.setFont(QtGui.QFont('Helvetica', 20))
        self.selectLabel.move(int((self.w / 2) - (self.cb.width() / 2)) + 7,
                              int((self.h / 2) - (self.cb.height() * 1.25)))
        self.selectLabel.adjustSize()

        self.connectBtn = QtWidgets.QPushButton(self)
        self.connectBtn.setText("Connect")
        self.connectBtn.setFont(QtGui.QFont('Helvetica', 14))
        self.connectBtn.setMinimumHeight(self.connectBtn.height() + 2)
        self.connectBtn.move(int((self.w / 2) - (self.connectBtn.width() / 2)),
                             int((self.h / 2) + (self.cb.height() * .5)) + 10)
        self.connectBtn.clicked.connect(self.connectAndInitiate)

        self.copyCodeBtn = CopyCodeBtn(self)
        self.copyCodeBtn.show()


    def connectAndInitiate(self):
        self.connectBtn.setText("Please Wait...")
        self.connectBtn.adjustSize()
        try:
            self.ser = serial.Serial(
                port=self.comPortList[self.cb.currentIndex()]['device'],
                baudrate=9600,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.SEVENBITS
            )
            self.ser.flush()
            self.ser.flushInput()
            self.ser.flushOutput()
            time.sleep(1)
            # self.ser.close()
            self.connectBtn.setText("Connected!")
            self.connectBtn.move(int((self.w / 2) - (self.connectBtn.width() / 2)),
                                 int((self.h / 2) + (self.cb.height() * .5)) + 10)
            self.arduinoIsConnected = True
        except:
            self.connectBtn.setText("Error, Please Choose Again")
            self.connectBtn.adjustSize()
            self.cb.model().item(self.cb.currentIndex()).setEnabled(False)
            self.connectBtn.move(int((self.w / 2) - (self.connectBtn.width() / 2)),
                                 int((self.h / 2) + (self.cb.height() * .5)) + 10)
            return
        if self.arduinoIsConnected is True:
            self.arduinoName = self.comPortList[self.cb.currentIndex()]['device']
            self.initMainApp(self.arduinoName, self.ser)

    @pyqtSlot()
    def initMainApp(self, value, ser):
        self.mainWindow = MainApplicationWindow(value, ser)
        self.mainWindow.show()
        self.close()


def window():
    app = QApplication(sys.argv)
    win = ConnectWindow()
    app.setStyle("fusion")

    # For Testing
    # win = MainApplicationWindow("")

    win.show()
    sys.exit(app.exec_())


window()
