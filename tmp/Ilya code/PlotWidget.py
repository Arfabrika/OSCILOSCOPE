# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)
from PySide6.QtCore import Slot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #  create widgets
        figure = Figure(figsize=(8, 6))
        #figure.set_size_inches(9, 7, forward=True)
        self.view = FigureCanvas(figure)
        self.axes = self.view.figure.subplots()
        self.axes.grid(True)
        self.toolbar = NavigationToolbar2QT(self.view, self)

        #  Create layout
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.view)
        self.setLayout(vlayout)

    def clear(self, x_scale = 0, y_scale = 0):
        if len(self.axes.lines):
            self.axes.clear()
            if (x_scale != 0):
                self.axes.set_xlim(-x_scale, x_scale)
            if y_scale != 0:
                self.axes.set_ylim(-y_scale, y_scale)
            
            self.axes.set_xlabel('Time, s')
            self.axes.set_ylabel('U, V')
            self.axes.grid(True)         
            self.view.draw()
