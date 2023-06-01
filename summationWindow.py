from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QDial
)
from PySide6.QtGui import QAction
from PlotWindow import PlotWindow

from SignalPlotWidget import SignalPlotWidget
from signalData import signalData, signalDataArray

class SummationWindow(QWidget):
    def __init__(self, DataArray, parent=None):
        super().__init__(parent)
        self.signalDataArray = DataArray
        self.signalsOnPlot = signalDataArray([])
        self.plot_window = PlotWindow()
        
        self.fs_signals_label = QLabel('Основной сигнал')
        self.fs_signals_list = QComboBox(self)
        #self.signals_list.addItems(signal_types)
        self.fs_signals_label.setBuddy(self.fs_signals_list)
        self.fs_signals_list.currentIndexChanged.connect(self.showSignalInfo_fs)
        # self.fs_signals_list.currentIndexChanged.connect(self.showSignalInfo_fs)

        fs_signals_layout = QHBoxLayout()
        fs_signals_layout.addWidget(self.fs_signals_label)
        fs_signals_layout.addWidget(self.fs_signals_list)

        self.fs_signal_form_combo = QLabel(self)
        self.fs_signal_form_combo_label = QLabel('Форма сигнала', self)
        self.fs_signal_form_combo_label.setBuddy(self.fs_signal_form_combo)

        fs_signals_form_layout = QHBoxLayout()
        fs_signals_form_layout.addWidget(self.fs_signal_form_combo_label)
        fs_signals_form_layout.addWidget(self.fs_signal_form_combo)

        self.fs_frequency_spin = QLabel()
        self.fs_frequency_label = QLabel('Частота')
        self.fs_frequency_label.setBuddy(self.fs_frequency_spin)

        fs_frequency_layout = QHBoxLayout()
        fs_frequency_layout.addWidget(self.fs_frequency_label)
        fs_frequency_layout.addWidget(self.fs_frequency_spin)

        self.fs_amplitude_spin = QLabel()
        self.fs_amplitude_label = QLabel('Амплитуда')
        self.fs_amplitude_label.setBuddy(self.fs_amplitude_spin)

        fs_amplitude_layout = QHBoxLayout()
        fs_amplitude_layout.addWidget(self.fs_amplitude_label)
        fs_amplitude_layout.addWidget(self.fs_amplitude_spin)


        fs_signal = QVBoxLayout()
        fs_signal.addLayout(fs_signals_layout)
        fs_signal.addLayout(fs_signals_form_layout)
        fs_signal.addLayout(fs_frequency_layout)
        fs_signal.addLayout(fs_amplitude_layout)

        self.show_plot_button = QPushButton('Показать график')
        self.show_plot_button.clicked.connect(self.show_plot)
        self.ok_button = QPushButton('Добавить сигнал')
        self.ok_button.clicked.connect(self.button_clicked)
        self.step_out_button = QPushButton('Убрать последний сигнал')
        self.step_out_button.clicked.connect(self.step_back)

        self.plot = SignalPlotWidget()

        signal_layout = QHBoxLayout()

        signal_layout.addLayout(fs_signal)

        main_layout = QVBoxLayout()

        mechanical_slider_amplitude_layout = QVBoxLayout()
        self.amplitude_lable = QLabel("ось y")
        self.mechanical_slider_amplitude = QDial()
        self.mechanical_slider_amplitude.setRange(0, 12)
        self.mechanical_slider_amplitude.setValue(6)
        mechanical_slider_amplitude_layout.addWidget(self.amplitude_lable)
        mechanical_slider_amplitude_layout.addWidget(self.mechanical_slider_amplitude)
        self.mechanical_slider_amplitude.valueChanged.connect(self.slider_frequency_move)
        
        mechanical_slider_frequency_layout = QVBoxLayout()
        self.frequency_lable = QLabel("ось x")
        self.mechanical_slider_frequency = QDial()
        self.mechanical_slider_frequency.setRange(0, 12)
        self.mechanical_slider_frequency.setValue(6)
        mechanical_slider_frequency_layout.addWidget(self.frequency_lable)
        mechanical_slider_frequency_layout.addWidget(self.mechanical_slider_frequency)
        self.mechanical_slider_frequency.valueChanged.connect(self.slider_frequency_move)
       
        mechanical_sliders = QVBoxLayout()

        mechanical_sliders.addLayout(mechanical_slider_frequency_layout)
        mechanical_sliders.addLayout(mechanical_slider_amplitude_layout)
        mechanical_sliders.addStretch(1)

        plot_layout = QHBoxLayout()
        plot_layout.addLayout(mechanical_sliders)
        plot_layout.addWidget(self.plot)

        
        main_layout.addLayout(signal_layout)
        main_layout.addWidget(self.show_plot_button)
        main_layout.addWidget(self.ok_button)
        main_layout.addWidget(self.step_out_button)
        main_layout.addLayout(plot_layout)

        self.setLayout(main_layout)
        self.setSignals()

        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

    def editScale(self):
        self.x_scale_value = float(self.scale_x.currentText())* 1.1
        self.y_scale_value = float(self.scale_y.currentText())* 1.1

        self.plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)
        self.plot.axes.set_xlim(-self.x_scale_value, self.x_scale_value)

        self.button_clicked()

    def updateSignalData(self, signalDataArray):
        self.signalDataArray = signalDataArray
        self.setSignals() 

    def setSignals(self):
        self.fs_signals_list.clear()
        data = self.signalDataArray.getArray()
        if len(data) == 0:
            self.fs_signals_list.addItem("Нет сигналов")
        else:   
            for i in range(len(data)):
                self.fs_signals_list.addItem('Сигнал ' + str(i + 1))
            self.showSignalInfo_fs()
    
    def button_clicked(self):
        curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData() 
       
        if self.signalsOnPlot.getArraySize() == 0:
            self.plot.plot(curSignal_fs[0], curSignal_fs[2], curSignal_fs[1], 1, animation_flag=0)
            self.signalsOnPlot.appendSignal(signalData(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], curSignal_fs[3], False))
        elif self.signalsOnPlot.getArraySize() == 1:
            ss_signal = self.signalsOnPlot.getSignalByIndex(self.signalsOnPlot.getArraySize() - 1)
            self.plot.polyharmonic(curSignal_fs[0], curSignal_fs[2], curSignal_fs[1], curSignal_fs[3],
                     ss_signal.getSignaType(), ss_signal.getAmplitude(), ss_signal.getFrequency(), ss_signal.getDuration())
            self.signalsOnPlot.appendSignal(signalData(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], curSignal_fs[3], False))
        else:
            self.plot.polyharmonic(curSignal_fs[0], curSignal_fs[2], curSignal_fs[1], curSignal_fs[3])

    def showSignalInfo_fs(self):
        if self.signalDataArray.getArraySize() > 0:
            curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData() 

            self.fs_amplitude_spin.setText(str(curSignal_fs[1]) + ' В')
            self.fs_frequency_spin.setText(str(curSignal_fs[2]) + ' Гц')
            self.fs_signal_form_combo.setText(curSignal_fs[0])
        else:
            self.fs_amplitude_spin.setText("Нет сигналов")
        
    def step_back(self):
        tmp = self.plot.remove_last_points()

        if tmp == True:
            return 
        

        lastSigData = self.signalsOnPlot.getLastSignal().getData()
        
        if lastSigData[1] == 0 or self.signalsOnPlot.getArraySize() == 1:
            self.signalsOnPlot.clear()
            self.plot.clear()
            return
        
        self.signalsOnPlot.removeLast()
       #bashkoff
    def slider_frequency_move(self):

        if self.mechanical_slider_frequency.value() % 2 == 0:
            self.x_scale_value = 0.0011 * 10**(self.mechanical_slider_frequency.value() // 2)
        else:
            self.x_scale_value = 0.0055 * 10**(self.mechanical_slider_frequency.value() // 2)

        if self.mechanical_slider_amplitude.value() % 2 == 0:
            self.y_scale_value = 0.0011 * 10**(self.mechanical_slider_amplitude.value() // 2)
        else:
            self.y_scale_value = 0.0055 * 10**(self.mechanical_slider_amplitude.value() // 2)

        self.plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)
        self.plot.axes.set_xlim(-self.x_scale_value, self.x_scale_value)

        self.plot.view.draw()
        self.plot.view.flush_events()

    def show_plot(self):
        if self.fs_signals_list.currentIndex() == -1:
            return 
        
        curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData()
        self.plot_window.plot_graph(curSignal_fs)
        self.plot_window.show()

    def closeEvent(self, event):
        self.plot.clear()
        self.fs_signals_list.setCurrentIndex(1)
        self.showSignalInfo_fs()
        print("Summation window closed")
