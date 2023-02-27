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

    def show_parametrs(self, formula):

        self.parametrs.setText(formula)
