import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCanvas


class Canvas(FigCanvas):

    def __init__(self, parent):
        fig = plt.figure(figsize=(4.8, 3.7))
        super(Canvas, self).__init__(fig)
        self.setParent(parent)
        fig.patch.set_facecolor("None")
        plt.style.use('bmh')

        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        plt.plot(t, s)
        fig.tight_layout()

        # plt.xlabel('time (s)')
        # plt.ylabel('voltage (mV)')
