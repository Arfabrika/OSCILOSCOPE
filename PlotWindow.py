from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QDial,
    QCheckBox
)

from SignalPlotWidget import SignalPlotWidget

class PlotWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signal_plot = SignalPlotWidget()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.signal_plot)

        self.setLayout(main_layout)

    def plot_graph(self, signalDataArray):
        self.signal_plot.clear()

        self.signal_plot.plot(signalDataArray[0], signalDataArray[2], signalDataArray[1], signalDataArray[3])
