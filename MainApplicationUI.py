import numpy as np
import serial
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel

from MatplotlibIntegrate import Canvas


class MainApplicationWindow(QMainWindow):
    
    slideLableRight: QLabel
    slideLableLeft: QLabel

    def __init__(self, comportName):
        self.w = 700
        self.h = 400

        self.comportName = comportName
        self.ser = serial.Serial(
            # port= self.comportName,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )

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

        self.expControlPanel = QtWidgets.QGroupBox(self)
        self.expControlPanel.resize(180, 180)
        self.expControlPanel.move(self.plotCanvas.x()+self.plotCanvas.width()+10, 15)
        self.expControlPanel.setTitle("Motor Controls")

        self.motorControlUI()

    def motorControlUI(self):
        panW = self.expControlPanel.width()
        panH = self.expControlPanel.height()

        sl = self.rotateSlider = QtWidgets.QSlider(self.expControlPanel)
        self.rotateSlider.setTickInterval(20)
        self.rotateSlider.setMinimum(0)
        self.rotateSlider.setMaximum(180)
        self.rotateSlider.setOrientation(1)
        self.rotateSlider.setTickPosition(1)
        self.rotateSlider.setFixedWidth(int(panW-(panW*0.2)))
        # self.rotateSlider.valueChanged.connect(lambda: print(self.rotateSlider.value()))
        self.rotateSlider.move(int((panW/2)-(self.rotateSlider.width()/2)),int((panH)-90))
        self.rotateSlider.setValue(0)
        self.rotateSlider.setSliderPosition(0)

        self.slideLableLeft = QtWidgets.QLabel(self.expControlPanel)
        self.slideLableLeft.setText("0°")
        self.slideLableLeft.move(int(sl.x())+3, sl.y()-20)

        self.slideLableRight = QtWidgets.QLabel(self.expControlPanel)
        self.slideLableRight.setText("180°")
        self.slideLableRight.move(int(sl.x() + sl.width() - self.slideLableRight.width()/5), sl.y() - 20)

        slValLab = self.slideValuelabel = QtWidgets.QLabel(self.expControlPanel)
        slValLab.setText('Degrees : 0° ')
        slValLab.move(int((self.expControlPanel.width()/2)-(self.slideValuelabel.width()/4)-8), int(self.rotateSlider.y()+(self.rotateSlider.height()/1.5)))
        sl.valueChanged.connect(self.updateLableValue)

        btnDegList = [45, 90, 135, 180]
        self.btnList = [2, 3, 4, 5]
        for i in np.arange(0,4):
            btn = QtWidgets.QPushButton(self)
            self.btnList[i] = btn
            self.btnList[i].setText(str(btnDegList[i])+"°")
            self.btnList[i].setFixedWidth(35)
            self.btnList[i].move(int(self.expControlPanel.x()+(i*(7+self.btnList[i].width())))+10, int(self.rotateSlider.y()-45))

        self.btnList[0].clicked.connect(lambda: self.updateValueWithButton(int(45)))
        self.btnList[1].clicked.connect(lambda: self.updateValueWithButton(int(90)))
        self.btnList[2].clicked.connect(lambda: self.updateValueWithButton(int(135)))
        self.btnList[3].clicked.connect(lambda: self.updateValueWithButton(int(180)))

        rtBtn = self.rotateSend = QtWidgets.QPushButton(self.expControlPanel)
        rtBtn.setText("Rotate Motor")
        rtBtn.adjustSize()
        rtBtn.move(int((panW/2)-(rtBtn.width()/2)+5), int(sl.y()+(slValLab.height()*2)-7))
        rtBtn.clicked.connect(self.startMotorRotation)

    def updateValueWithButton(self, value):
        self.rotateSlider.setSliderPosition(int(value))
        self.rotateSlider.setValue(int(value))
        self.updateLableValue()

    def updateLableValue(self):
        self.rotateSlider.valueChanged.connect(lambda: self.slideValuelabel.setText('Degres : '+str(self.rotateSlider.value())+'°'))
        self.slideValuelabel.adjustSize()
        self.slideValuelabel.move(int((self.expControlPanel.width()/2)-(self.slideValuelabel.width()/4)-10), self.slideValuelabel.y())
        print(self.rotateSlider.value())

    def startMotorRotation(self):
        print('cool')

