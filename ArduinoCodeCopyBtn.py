import time

from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QApplication


class CopyCodeBtn(QPushButton):

    def __init__(self, parent):
        super(CopyCodeBtn, self).__init__()

        self.setParent(parent)
        self.setText('Copy Arduino Code')
        self.setIcon(QIcon('arduinoIcon.png'))
        self.setIconSize(QSize(30, 30))
        self.adjustSize()
        self.move(parent.width()-15-self.width(), parent.height()-10-self.height())

        self.clicked.connect(self.copyCode)

    def copyCode(self):
        QApplication.clipboard().setText('NO CODE FOUND YET')

        orignalText = self.text()
        self.setText('Copied!')