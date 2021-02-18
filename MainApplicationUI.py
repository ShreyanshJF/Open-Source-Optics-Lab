import re
import sys
import time
import traceback

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from MatplotlibIntegrate import Canvas, CanvasNav


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(str)
    progress = pyqtSignal(list)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['error_callback'] = self.signals.error
        self.kwargs['result_callback'] = self.signals.result

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit()


class MainApplicationWindow(QMainWindow):

    def __init__(self, comportName, ser):
        self.collectedData = []
        self.currentDegMove = 0
        self.finishedStepsOf5 = 0
        self.w = 700
        self.h = 420

        self.comportName = comportName

        self.ser = ser
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        time.sleep(1)

        self.stepsOf5 = 0

        super(MainApplicationWindow, self).__init__()
        # self.setGeometry(300, 200, self.w, self.h)
        self.setFixedSize(self.w, self.h)
        self.setWindowTitle("Open Source Lab | Optics")

        self.threadPool = QThreadPool()

        self.xData = []
        self.yData = []
        self.dataPlotRef = None
        self.initUI()

    def initUI(self):

        self.plotCanvas = Canvas(self)
        # self.plotCanvas.resize(480, 370)
        # self.plotCanvas.move(15, 15)
        self.plotCanvas.setStyleSheet("background-color:transparent;")
        self.plotCanvas.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.dataPlotRef = self.plotCanvas.plt.plot(self.xData, self.yData)
        self.dataPlotRef = self.dataPlotRef[0]
        self.plotCanvas.plt.tight_layout()

        self.canvasNav = CanvasNav(self.plotCanvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvasNav)
        layout.addWidget(self.plotCanvas)

        self.plotParent = QtWidgets.QWidget(self)
        self.plotParent.setLayout(layout)
        self.plotParent.resize(480, 375)
        self.plotParent.move(10, 15)

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
        self.dataUI()

        self.referenceCurvePanel = QtWidgets.QGroupBox(self)
        self.referenceCurvePanel.resize(180, 70)
        self.referenceCurvePanel.move(self.plotCanvas.x() + self.plotCanvas.width() + 5,
                                      25 + self.motorControlPanel.height() + self.dataPanel.height())
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
        self.rotateSlider.setFixedWidth(int(panW - (panW * 0.2)))
        self.rotateSlider.move(int((panW / 2) - (self.rotateSlider.width() / 2)), int((panH) - 90))

        slValLab = self.slideValuelabel = QtWidgets.QLabel(self.motorControlPanel)
        slValLab.setText('Degres : ' + str(self.rotateSlider.value()) + '°')
        slValLab.move(int((self.motorControlPanel.width() / 2) - (self.slideValuelabel.width() / 4) - 8),
                      int(self.rotateSlider.y() + (self.rotateSlider.height() / 1.5)))

        sl.valueChanged.connect(self.updateLableValue)

        self.slideLabelLeft = QtWidgets.QLabel(self.motorControlPanel)
        self.slideLabelLeft.setText("0°")
        self.slideLabelLeft.move(int(sl.x()) + 3, sl.y() - 20)

        self.slideLabelRight = QtWidgets.QLabel(self.motorControlPanel)
        self.slideLabelRight.setText("180°")
        self.slideLabelRight.move(int(sl.x() + sl.width() - self.slideLabelRight.width() / 5), sl.y() - 20)

        btnDegList = [45, 90, 135, 180]
        self.btnList = [2, 3, 4, 5]
        for i in np.arange(0, 4):
            btn = QtWidgets.QPushButton(self)
            self.btnList[i] = btn
            self.btnList[i].setText(str(btnDegList[i]) + "°")
            self.btnList[i].setFixedWidth(35)
            self.btnList[i].move(int(self.motorControlPanel.x() + (i * (7 + self.btnList[i].width()))) + 10,
                                 int(self.rotateSlider.y() - 45))

        self.btnList[0].clicked.connect(lambda: self.updateValueWithButton(int(45)))
        self.btnList[1].clicked.connect(lambda: self.updateValueWithButton(int(90)))
        self.btnList[2].clicked.connect(lambda: self.updateValueWithButton(int(135)))
        self.btnList[3].clicked.connect(lambda: self.updateValueWithButton(int(180)))

        rtBtn = self.rotateSend = QtWidgets.QPushButton(self.motorControlPanel)
        rtBtn.setText("Turn Motor + Plot Data")
        rtBtn.adjustSize()
        rtBtn.setStyleSheet("background-color: rgb(140, 255, 140)")
        rtBtn.move(int((panW / 2) - (rtBtn.width() / 2) + 5), int(sl.y() + (slValLab.height() * 2) - 7))
        rtBtn.clicked.connect(lambda: self.startMotorRotation(self.rotateSlider.value()))

        self.updateLableValue()

    def updateLableValue(self):
        self.slideValuelabel.setText('Degres : ' + str(self.rotateSlider.value()) + '°')
        self.slideValuelabel.adjustSize()
        self.slideValuelabel.move(int((self.motorControlPanel.width() / 2) - (self.slideValuelabel.width() / 4) - 10),
                                  self.slideValuelabel.y())

    def roundTo5(self):
        newValue = np.around(self.rotateSlider.value() / 5, decimals=0) * 5
        self.rotateSlider.setValue(newValue)
        self.updateLableValue()

    def dataUI(self):

        parent = self.dataPanel

        self.fitCurveBtn = QtWidgets.QPushButton(parent)
        self.fitCurveBtn.setText("Fit Cos²")
        self.fitCurveBtn.adjustSize()
        self.fitCurveBtn.move(12, int(parent.height() / 3 - 3))

        self.clearGraphBtn = QtWidgets.QPushButton(parent)
        self.clearGraphBtn.setText("Reset All")
        self.clearGraphBtn.adjustSize()
        self.clearGraphBtn.move(12, int(parent.height() - self.clearGraphBtn.height() - 10))

        self.exportDataBtn = QtWidgets.QPushButton(parent)
        self.exportDataBtn.setText("Export")
        self.exportDataBtn.adjustSize()
        self.exportDataBtn.setFixedWidth(self.exportDataBtn.width() - 15)
        self.exportDataBtn.move(parent.width() - 12 - self.exportDataBtn.width(),
                                int(parent.height() - self.exportDataBtn.height() - 10))

        self.fitCurveBtn = QtWidgets.QCheckBox(parent)
        self.fitCurveBtn.setText("Hide Fit")
        self.fitCurveBtn.adjustSize()
        self.fitCurveBtn.move(parent.width() - 14 - self.exportDataBtn.width(), int(parent.height() / 3 - 3))

    def referenceUI(self):

        parent = self.referenceCurvePanel

        self.selectCurve = QtWidgets.QComboBox(parent)
        self.selectCurve.addItem("Cos²", "cos")
        self.selectCurve.addItem("Sin²", "sin")
        self.selectCurve.adjustSize()
        self.selectCurve.setFixedWidth(self.selectCurve.width() + 5)
        self.selectCurve.move(12, int(parent.height() / 2 - 3))
        self.selectCurve.setCurrentIndex(0)

        self.plotBtn = QtWidgets.QPushButton(parent)
        self.plotBtn.setText("Plot Curve")
        self.plotBtn.adjustSize()
        self.plotBtn.move(parent.width() - 12 - self.plotBtn.width(), int(parent.height() / 2 - 3))

    def updateValueWithButton(self, value):
        self.rotateSlider.setValue(int(value))
        self.rotateSlider.valueChanged.connect(
            lambda: self.slideValuelabel.setText('Degres : ' + str(self.rotateSlider.value()) + '°'))
        self.slideValuelabel.adjustSize()
        self.slideValuelabel.move(int((self.motorControlPanel.width() / 2) - (self.slideValuelabel.width() / 4) - 10),
                                  self.slideValuelabel.y())

    def disableMotorControls(self, boolVal):
        if boolVal == True:
            turnBtn = self.rotateSend
            turnBtn.setStyleSheet("background-color: rgb(255, 255, 140)")
            turnBtn.setText("Collecting data...")
            turnBtn.adjustSize()
            turnBtn.move(int((self.motorControlPanel.width() / 2) - (turnBtn.width() / 2) + 5),
                         int(self.rotateSlider.y() + (self.slideValuelabel.height() * 3.8) - 7))

            self.motorControlPanel.setDisabled(boolVal)
            for i in self.btnList:
                i.setDisabled(boolVal)
        else:
            turnBtn = self.rotateSend
            turnBtn.setStyleSheet("background-color: rgb(140, 255, 140)")
            turnBtn.setText("Turn Motor + Plot Data")
            turnBtn.adjustSize()
            turnBtn.move(int((self.motorControlPanel.width() / 2) - (turnBtn.width() / 2) + 5),
                         int(self.rotateSlider.y() + (self.slideValuelabel.height() * 3.8) - 7))

            self.motorControlPanel.setDisabled(boolVal)
            for i in self.btnList:
                i.setDisabled(boolVal)

    def arduinoRunner(self, deg, progress_callback, error_callback, result_callback):

        totalSteps = int(deg * 5.625)
        self.stepsOf5 = np.round(totalSteps / 5)
        self.finishedStepsOf5 = 0
        steps = 5

        print(self.stepsOf5)
        self.ser.write((str(steps) + "\x04").encode("utf-8"))

        while True:

            inputFromArduino = self.ser.readline()
            if inputFromArduino:
                inputFromArduino = inputFromArduino.decode("utf-8")
                inputFromArduino = inputFromArduino.strip()
            if "potentio" in inputFromArduino:  # to print potentiometer value
                res = int(re.search(r'\d+$', inputFromArduino).group())
                entry = [(self.finishedStepsOf5 + 1)*5/5.625, res]
                progress_callback.emit(entry)
            if inputFromArduino == 'DONE':
                self.stepsOf5 = self.stepsOf5 - 1
                self.finishedStepsOf5 = self.finishedStepsOf5 + 1
                if self.stepsOf5 == 0:
                    break
                self.ser.write((str(steps) + "\x04").encode("utf-8"))

            # result_callback.emit('5x Steps Left: {} | Res: {} '.format(self.stepsOf5, re.search(r'\d+$', inputFromArduino)))

    def updateGraph(self, newEntry):
        self.collectedData.append(newEntry)
        data = np.transpose(self.collectedData)
        self.plotCanvas.plt.cla()
        if data.any():
            self.plotCanvas.plt.scatter(data[0], data[1], color='C2')
            self.plotCanvas.plt.xlim(0,self.currentDegMove+5,min)
        self.plotCanvas.draw()
        print(np.transpose(data))

    def print_output(self, p):
        print(p)

    def startMotorRotation(self, deg):
        self.roundTo5()

        self.disableMotorControls(True)

        self.collectedData = []

        self.currentDegMove = deg

        print('Starting Worker')

        worker = Worker(self.arduinoRunner, deg)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.error.connect(self.print_output)
        worker.signals.finished.connect(lambda: self.disableMotorControls(False))
        worker.signals.finished.connect(lambda: print(self.collectedData))
        worker.signals.progress.connect(self.updateGraph)

        self.threadPool.start(worker)
        print(self.collectedData)

        # self.ser.close()  # Serial Close after while loop
