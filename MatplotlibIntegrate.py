import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as CanvasNavDefault
from matplotlib.figure import Figure


def cos2Fnc(val, A, B, C, D):
    return A * (np.cos((B * val) + C) ** 2) + D


class CanvasNav(CanvasNavDefault):

    toolitems = [t for t in CanvasNavDefault.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]


class Canvas(FigCanvas):

    def __init__(self, parent):
        fig = plt.figure(figsize=(4.8, 3.5))
        super(Canvas, self).__init__(fig)

        self.plt = plt
        fig.patch.set_facecolor("None")
        self.plt.style.use('bmh')
        self.plt.xlim(0, 90)
        self.plt.ylim(0, 1)
        self.plt.xlabel("Degrees of Rotation")
        self.plt.ylabel("Intensity")
