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

class ParametrWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parametrs = QLabel()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.parametrs)

        self.setLayout(main_layout)
        self.setWindowTitle('Параметры АМ')
        self.setFixedWidth(300)

    def show_parametrs(self, fs_DataArray, ss_dataArray):
        UMax = fs_DataArray[1] + ss_dataArray[1]
        Umin = fs_DataArray[1] - ss_dataArray[1]
        M = round(ss_dataArray[1] / fs_DataArray[1], 2)

        self.parametrs.setText('Umax = Uн + Uм = ' + str(UMax) + '\nUmin = Uн - Uм = ' + str(Umin) + '\nM = Uм / Uн = ' + str(M) + '\n')
