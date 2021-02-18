import time

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QApplication


class CopyCodeBtn(QPushButton):

    def __init__(self, parent):
        super(CopyCodeBtn, self).__init__()

        self.setParent(parent)
        self.setText(' Arduino Code')
        self.setIcon(QIcon('arduinoIcon.png'))
        self.setIconSize(QSize(30, 30))
        self.adjustSize()
        self.move(parent.width() - 15 - self.width(), parent.height() - 10 - self.height())

        self.clicked.connect(self.copyCode)

    def copyCode(self):
        self.openUrl()

    def openUrl(self):
        parent = self.parent()
        url = QtCore.QUrl('https://pastebin.com/kF6z0Ptc')
        if not QtGui.QDesktopServices.openUrl(url):
            self.setText('Open Url Could not open url')
            self.adjustSize()
            self.move(parent.width() - 15 - self.width(), parent.height() - 10 - self.height())
