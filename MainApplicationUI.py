from os import wait

import numpy as np
import serial
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel
import time

from MatplotlibIntegrate import Canvas


class MainApplicationWindow(QMainWindow):
    
    slideLableRight: QLabel
    slideLableLeft: QLabel

    def __init__(self, comportName):
        self.w = 700
        self.h = 420

        self.comportName = comportName
        self.ser = ""

        super(MainApplicationWindow, self).__init__()
        # self.setGeometry(300, 200, self.w, self.h)
        self.setFixedSize(self.w, self.h)
        self.setWindowTitle("Open Source Lab | Optics")
        self.initUI()

    def initUI(self):
        self.plotCanvas = Canvas(self)
        # self.plotCanvas.resize(480, 370)
        self.plotCanvas.move(15, 15)
        self.plotCanvas.setStyleSheet("background-color:transparent;")
        self.plotCanvas.setStyleSheet("background-color: rgba(0,0,0,0);")

        self.motorControlPanel = QtWidgets.QGroupBox(self)
        self.motorControlPanel.resize(180, 180)
        self.motorControlPanel.move(self.plotCanvas.x() + self.plotCanvas.width() + 5, 15)
        self.motorControlPanel.setTitle("Motor Controls")
        self.motorControlUI()

        self.dataPanel = QtWidgets.QGroupBox(self)
        self.dataPanel.resize(180, 100)
        self.dataPanel.move(self.plotCanvas.x() + self.plotCanvas.width() + 5, 20 + self.motorControlPanel.height())
        self.dataPanel.setTitle("Data")
        self.dataPanel.setDisabled(True)

        self.referenceCurvePanel = QtWidgets.QGroupBox(self)
        self.referenceCurvePanel.resize(180, 70)
        self.referenceCurvePanel.move(self.plotCanvas.x() + self.plotCanvas.width() + 5, 25 + self.motorControlPanel.height() + self.dataPanel.height())
        self.referenceCurvePanel.setTitle("Refrence Curve")
        self.referenceCurvePanel.setDisabled(True)
        self.referenceUI()

    def motorControlUI(self):
        panW = self.motorControlPanel.width()
        panH = self.motorControlPanel.height()

        sl = self.rotateSlider = QtWidgets.QSlider(self.motorControlPanel)
        self.rotateSlider.setMinimum(0)
        self.rotateSlider.setMaximum(180)
        self.rotateSlider.setOrientation(1)
        self.rotateSlider.setTickPosition(1)
        self.rotateSlider.setFixedWidth(int(panW-(panW*0.2)))
        self.rotateSlider.move(int((panW/2)-(self.rotateSlider.width()/2)),int((panH)-90))

        slValLab = self.slideValuelabel = QtWidgets.QLabel(self.motorControlPanel)
        slValLab.setText('Degres : ' + str(self.rotateSlider.value()) + '°')
        slValLab.move(int((self.motorControlPanel.width() / 2) - (self.slideValuelabel.width() / 4) - 8),
                      int(self.rotateSlider.y() + (self.rotateSlider.height() / 1.5)))


        sl.valueChanged.connect(self.updateLableValue)

        self.slideLableLeft = QtWidgets.QLabel(self.motorControlPanel)
        self.slideLableLeft.setText("0°")
        self.slideLableLeft.move(int(sl.x())+3, sl.y()-20)

        self.slideLableRight = QtWidgets.QLabel(self.motorControlPanel)
        self.slideLableRight.setText("180°")
        self.slideLableRight.move(int(sl.x() + sl.width() - self.slideLableRight.width()/5), sl.y() - 20)



        btnDegList = [45, 90, 135, 180]
        self.btnList = [2, 3, 4, 5]
        for i in np.arange(0,4):
            btn = QtWidgets.QPushButton(self)
            self.btnList[i] = btn
            self.btnList[i].setText(str(btnDegList[i])+"°")
            self.btnList[i].setFixedWidth(35)
            self.btnList[i].move(int(self.motorControlPanel.x() + (i * (7 + self.btnList[i].width()))) + 10, int(self.rotateSlider.y() - 45))

        self.btnList[0].clicked.connect(lambda: self.updateValueWithButton(int(45)))
        self.btnList[1].clicked.connect(lambda: self.updateValueWithButton(int(90)))
        self.btnList[2].clicked.connect(lambda: self.updateValueWithButton(int(135)))
        self.btnList[3].clicked.connect(lambda: self.updateValueWithButton(int(180)))

        rtBtn = self.rotateSend = QtWidgets.QPushButton(self.motorControlPanel)
        rtBtn.setText("Turn Motor + Plot Data")
        rtBtn.adjustSize()
        rtBtn.setStyleSheet("background-color: rgb(140, 255, 140)")
        rtBtn.move(int((panW/2)-(rtBtn.width()/2)+5), int(sl.y()+(slValLab.height()*2)-7))
        rtBtn.clicked.connect(lambda: self.startMotorRotation(self.rotateSlider.value()))

        self.updateLableValue()

    def updateLableValue(self):
        self.slideValuelabel.setText('Degres : ' + str(self.rotateSlider.value()) + '°')
        self.slideValuelabel.adjustSize()
        self.slideValuelabel.move(int((self.motorControlPanel.width() / 2) - (self.slideValuelabel.width() / 4) - 10), self.slideValuelabel.y())

    def roundTo5(self):
        newValue = np.around(self.rotateSlider.value() / 5, decimals=0) * 5
        self.rotateSlider.setValue(newValue)
        self.updateLableValue()

    # def dataUI(self):

    def referenceUI(self):

        parent = self.referenceCurvePanel

        self.selectCurve = QtWidgets.QComboBox(parent)
        self.selectCurve.addItem("Cos²", "cos")
        self.selectCurve.addItem("Sin²", "sin")
        self.selectCurve.adjustSize()
        self.selectCurve.setFixedWidth(self.selectCurve.width()+5)
        self.selectCurve.move(12, int(parent.height()/2-3))
        self.selectCurve.setCurrentIndex(0)

        self.plotBtn = QtWidgets.QPushButton(parent)
        self.plotBtn.setText("Plot Curve")
        self.plotBtn.adjustSize()
        self.plotBtn.move(parent.width()-12-self.plotBtn.width(), int(parent.height()/2-3))


    def updateValueWithButton(self, value):
        self.rotateSlider.setValue(int(value))
        self.rotateSlider.valueChanged.connect(lambda: self.slideValuelabel.setText('Degres : ' + str(self.rotateSlider.value()) + '°'))
        self.slideValuelabel.adjustSize()
        self.slideValuelabel.move(int((self.motorControlPanel.width() / 2) - (self.slideValuelabel.width() / 4) - 10),
                                  self.slideValuelabel.y())


    def startMotorRotation(self, deg):
        self.roundTo5()

        turnBtn = self.rotateSend
        turnBtn.setStyleSheet("background-color: 255, 100, 255")
        turnBtn.setText("Collecting data...")
        turnBtn.adjustSize()
        turnBtn.move(int((self.motorControlPanel.width() / 2) - (turnBtn.width() / 2) + 5), int(self.rotateSlider.y() + (self.slideValuelabel.height() * 3.8) - 7))

        self.motorControlPanel.setDisabled(True)
        for i in self.btnList:
            i.setDisabled(True)

        self.ser = serial.Serial(
            port=self.comportName,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

        # totalSteps = int(deg*5.625)
        # stepsOf5 = np.round(totalSteps/5)
        # lastSpteps = totalSteps - (stepsOf5*5)
        # potentioData = []
        #
        # while stepsOf5 > 0:
        #
        #     step = 5
        #
        #     ser.write((str(step) + "\x04").encode("utf-8"))
        #     inputfromarduino = ser.readline()
        #
        #     if inputfromarduino:
        #         inputfromarduino = inputfromarduino.decode("utf-8")
        #         inputfromarduino = inputfromarduino.strip()
        #
        #     if "potentio" in inputfromarduino:  # to print potentiometer value
        #         print(inputfromarduino)
        #
        #     if (inputfromarduino == 'DONE'):
        #         steps = 5
        #         ser.write((str(steps) + "\x04").encode("utf-8"))
        self.ser.close()

