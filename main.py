
import sys
import time

import serial
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow

from ArduinoCodeCopyBtn import CopyCodeBtn
from MainApplicationUI import MainApplicationWindow
from comPortSetup import getComportsList

import qtawesome as qta

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
        self.cb.move(int((self.w / 2) - (self.cb.width() / 2))-20, int((self.h / 2) - (self.cb.height() / 2)))

        self.selectLabel = QtWidgets.QLabel(self)
        self.selectLabel.setText("Select Arduino Com Port")
        self.selectLabel.setFont(QtGui.QFont('Helvetica', 20))
        self.selectLabel.move(int((self.w / 2) - (self.cb.width() / 2)) -13,
                              int((self.h / 2) - (self.cb.height() * 1.25)))
        self.selectLabel.adjustSize()

        self.refreshBtn = QtWidgets.QPushButton(self)
        self.refreshBtn.setIcon(qta.icon('mdi.refresh'))
        self.refreshBtn.adjustSize()
        self.refreshBtn.setFixedWidth(40)
        self.refreshBtn.move(self.cb.x()+5+self.cb.width(), int(self.cb.y()))
        self.refreshBtn.clicked.connect(self.refreshComList)

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

    def refreshComList(self):
        self.comPortList.clear()
        self.comPortList = getComportsList()
        self.cb.clear()
        h = self.cb.height()
        for i in self.comPortList:
            self.cb.addItem("Name : " + str(i["name"]) + " (Manufacturer : " + str(i["manufacturer"]) + ")",
                            i["device"])
        self.cb.adjustSize()
        self.cb.setMinimumHeight(h)
        self.cb.move(int((self.w / 2) - (self.cb.width() / 2))-20, int((self.h / 2) - (self.cb.height() / 2)))
        self.refreshBtn.move(self.cb.x() + 5 + self.cb.width(), int(self.cb.y()))

    @pyqtSlot()
    def initMainApp(self, value, ser):
        self.mainWindow = MainApplicationWindow(value, ser)
        self.mainWindow.show()
        self.close()


def window():
    app = QApplication(sys.argv)
    win = ConnectWindow()
    app.setStyle("fusion")

    win.show()
    sys.exit(app.exec_())


window()
