import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCanvas


def cos2Fnc(val, A, B, C, D):
    return A * (np.cos((B * val) + C) ** 2) + D


class Canvas(FigCanvas):

    def __init__(self, parent):
        fig = plt.figure(figsize=(4.8, 3.9))
        super(Canvas, self).__init__(fig)
        self.setParent(parent)
        fig.patch.set_facecolor("None")
        plt.style.use('bmh')
        # t = np.arange(0.0, 2.0, 0.01)
        # s = 1 + cos2Fnc(t, 1, 1, 0, 0)

        # plt.plot(t, s, label="Name")
        try:
            plt.legend()
        except:
            pass
        fig.tight_layout()

        # plt.xlabel('time (s)')
        # plt.ylabel('voltage (mV)')
        plt.xlim(0,180)
