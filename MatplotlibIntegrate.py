import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as CanvasNavDefault
from matplotlib.figure import Figure


def cos2Fnc(val, A, B, C, D):
    return A * (np.cos((B * val) + C) ** 2) + D


class CanvasNav(CanvasNavDefault):

    print(CanvasNavDefault.toolitems)
    toolitems = [t for t in CanvasNavDefault.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]


class Canvas(FigCanvas):

    def __init__(self, parent):
        fig = plt.figure(figsize=(4.95, 4))
        super(Canvas, self).__init__(fig)

        self.plt = plt
        fig.patch.set_facecolor("None")
        self.plt.style.use('bmh')
