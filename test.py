# import sys
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from PyQt5.QtWidgets import QApplication, QWidget
# import matplotlib.animation as animation
# from matplotlib import style
#
#
#
# app = QApplication(sys.argv)
# demo = AppDemo()
# demo.show()
# sys.exit(app.exec_())


import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCanvas
from PyQt5.QtWidgets import QApplication, QWidget

class Canvas(FigCanvas):

    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 4))
        super(Canvas, self).__init__(fig)
        self.setParent(parent)

        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        self.ax.plot(t, s)

        self.ax.set(xlabel='time (s)', ylabel='voltage (mV)',
                    title='About as simple as it gets, folks')
        self.ax.grid()


class AppDemo(QWidget):
    def __init__(self):
        super(AppDemo, self).__init__()
        self.resize(700, 400)

        chart = Canvas(self)

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())



