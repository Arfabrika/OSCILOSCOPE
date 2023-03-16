from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
    QDial
)
from PySide6.QtGui import QAction
from ParametrWindow import ParametrWindow
from PlotWindow import PlotWindow

from SignalPlotWidget import SignalPlotWidget
from SpectrePlotWidget import SpectrePlotWidget
from scalefuncs import *

class FrequencyWindow(QWidget):
    def __init__(self, signalDataArray, parent=None):
        super().__init__(parent)
        self.signalDataArray = signalDataArray
        self.plot_window = PlotWindow()
        self.parametr_window = ParametrWindow()

        self.fs_signals_label = QLabel('Основной сигнал')
        self.fs_signals_list = QComboBox(self)
        self.fs_signals_label.setBuddy(self.fs_signals_list)
        self.fs_signals_list.currentIndexChanged.connect(self.showSignalInfo_fs)

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
        self.fs_frequency_label = QLabel('Частота f, Гц')
        self.fs_frequency_label.setBuddy(self.fs_frequency_spin)

        fs_frequency_layout = QHBoxLayout()
        fs_frequency_layout.addWidget(self.fs_frequency_label)
        fs_frequency_layout.addWidget(self.fs_frequency_spin)

        self.fs_amplitude_spin = QLabel()
        self.fs_amplitude_label = QLabel('Амплитуда Uн, В')
        self.fs_amplitude_label.setBuddy(self.fs_amplitude_spin)

        fs_amplitude_layout = QHBoxLayout()
        fs_amplitude_layout.addWidget(self.fs_amplitude_label)
        fs_amplitude_layout.addWidget(self.fs_amplitude_spin)

        self.plot1_button = QPushButton('Показать график')
        self.plot1_button.clicked.connect(self.show_plot1)

        self.formula = QLabel('Общая формула ЧМ: u(t) = Uн * cos(2*pi*f*t + m*sin(2*pi*F*t))')

        self.signal_plot = SignalPlotWidget()

        fs_signal = QVBoxLayout()
        fs_signal.addLayout(fs_signals_layout)
        fs_signal.addLayout(fs_signals_form_layout)
        fs_signal.addLayout(fs_frequency_layout)
        fs_signal.addLayout(fs_amplitude_layout)

        deviation_layout = QHBoxLayout()
        self.deviation_label = QLabel("Частота девиации:")
        self.deviation_input = QSpinBox()
        deviation_layout.addWidget(self.deviation_label)
        deviation_layout.addWidget(self.deviation_input)
        fs_signal.addLayout(deviation_layout)
        fs_signal.addWidget(self.plot1_button)
        fs_signal.addWidget(self.formula)
        fs_signal.addWidget(self.signal_plot)

        self.ss_signals_label = QLabel('Модулирующий сигнал')
        self.ss_signals_list = QComboBox(self)
        self.ss_signals_label.setBuddy(self.ss_signals_list)
        self.ss_signals_list.currentIndexChanged.connect(self.showSignalInfo_ss)

        ss_signals_layout = QHBoxLayout()
        ss_signals_layout.addWidget(self.ss_signals_label)
        ss_signals_layout.addWidget(self.ss_signals_list)

        self.ss_signal_form_combo = QLabel(self)
        self.ss_signal_form_combo_label = QLabel('Форма сигнала', self)
        self.ss_signal_form_combo_label.setBuddy(self.ss_signal_form_combo)

        ss_signals_form_layout = QHBoxLayout()
        ss_signals_form_layout.addWidget(self.ss_signal_form_combo_label)
        ss_signals_form_layout.addWidget(self.ss_signal_form_combo)

        self.ss_frequency_spin = QLabel()
        self.ss_frequency_label = QLabel('Частота F, Гц')
        self.ss_frequency_label.setBuddy(self.ss_frequency_spin)

        ss_frequency_layout = QHBoxLayout()
        ss_frequency_layout.addWidget(self.ss_frequency_label)
        ss_frequency_layout.addWidget(self.ss_frequency_spin)

        self.ss_amplitude_spin = QLabel()
        self.ss_amplitude_label = QLabel('Амплитуда Um, B')
        self.ss_amplitude_label.setBuddy(self.ss_amplitude_spin)

        ss_amplitude_layout = QHBoxLayout()
        ss_amplitude_layout.addWidget(self.ss_amplitude_label)
        ss_amplitude_layout.addWidget(self.ss_amplitude_spin)

        self.plot2_button = QPushButton('Показать график')
        self.plot2_button.clicked.connect(self.show_plot2)

        self.formula_spectr = QLabel('Общая формула ЧМ: u(t) = Uн * cos(2*pi*f*t) + (Uн * m/2) * cos((2*pi*f + 2*pi*F)t) + (Uн * m/2) * cos((2*pi*f - 2*pi*F)t)')

        self.specter_plot = SpectrePlotWidget()

        self.ss_empty = QLabel(" ")

        ss_signal = QVBoxLayout()
        ss_signal.addLayout(ss_signals_layout)
        ss_signal.addLayout(ss_signals_form_layout)
        ss_signal.addLayout(ss_frequency_layout)
        ss_signal.addLayout(ss_amplitude_layout)
        ss_signal.addWidget(self.ss_empty)
        ss_signal.addWidget(self.plot2_button)
        ss_signal.addWidget(self.formula_spectr)
        ss_signal.addWidget(self.specter_plot)

        self.ok_button = QPushButton('Выполнить модуляцию')
        self.ok_button.clicked.connect(self.ok_button_clicked)

        self.parametrs = QPushButton('Показать параметры сигнала')
        self.parametrs.clicked.connect(self.show_parametrs_button)

        signal_layout = QHBoxLayout()        
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
        mechanical_sliders.addStretch(2)
        mechanical_sliders.addLayout(mechanical_slider_frequency_layout)
        mechanical_sliders.addLayout(mechanical_slider_amplitude_layout)
        mechanical_sliders.addStretch(1)

        signal_layout.addLayout(fs_signal)
        signal_layout.addLayout(ss_signal)

        main_layout = QVBoxLayout()
        main_layout.addLayout(signal_layout)

        main_layout.addWidget(self.ok_button)
        main_layout.addWidget(self.parametrs)
        
        tmp = QHBoxLayout() 
        tmp.addLayout(mechanical_sliders)
        tmp.addLayout(main_layout)

        self.x_scale_value = 1
        self.y_scale_value = 1

        self.deviation_input.setValue(10)
        self.setLayout(tmp)

        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

    def updateSignalData(self, signalDataArray):
        self.signalDataArray = signalDataArray
        self.setSignals()

    def closeEvent(self, event):
        event.accept()

    def editScale(self):
        cur_x_scale = float(self.scale_x.currentText())
        cur_y_scale = float(self.scale_y.currentText())
        self.x_scale_value = cur_x_scale * 1.1
        self.y_scale_value = cur_y_scale * 1.1                

        self.ok_button_clicked()
       
    def setSignals(self):
        self.fs_signals_list.clear()
        self.ss_signals_list.clear()
        data = self.signalDataArray.getArray()
        if len(data) == 0:
            self.fs_signals_list.addItem("Нет сигналов")
            self.ss_signals_list.addItem("Нет сигналов")
        else:
            for i in range(len(data)):
                self.fs_signals_list.addItem('Сигнал ' + str(i + 1))
                self.ss_signals_list.addItem('Сигнал ' + str(i + 1))

    def showSignalInfo_fs(self):
        if len(self.signalDataArray.getArray()) > 0:
            curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData() 

            self.fs_amplitude_spin.setText(str(curSignal_fs[1]))
            self.fs_frequency_spin.setText(str(curSignal_fs[2]))
            self.fs_signal_form_combo.setText(curSignal_fs[0])
    
    def show_plot1(self):
        if self.fs_signals_list.currentIndex() == -1:
            return 
        
        curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData()
        self.plot_window.plot_graph(curSignal_fs)
        self.plot_window.show()

    def showSignalInfo_ss(self):
        if len(self.signalDataArray.getArray()) > 0:
            curSignal_ss = self.signalDataArray.getSignalByIndex(self.ss_signals_list.currentIndex()).getData() 

            self.ss_amplitude_spin.setText(str(curSignal_ss[1]))
            self.ss_frequency_spin.setText(str(curSignal_ss[2]))
            self.ss_signal_form_combo.setText(curSignal_ss[0])

    def show_plot2(self):
        if self.fs_signals_list.currentIndex() == -1:
            return 
        
        curSignal_ss = self.signalDataArray.getSignalByIndex(self.ss_signals_list.currentIndex()).getData()
        self.plot_window.plot_graph(curSignal_ss)
        self.plot_window.show()

    def ok_button_clicked(self):
        ind_fs = self.fs_signals_list.currentIndex()
        ind_ss = self.ss_signals_list.currentIndex()
        signal_fs = self.signalDataArray.getSignalByIndex(ind_fs).getData()
        signal_ss = self.signalDataArray.getSignalByIndex(ind_ss).getData()
        freq_dev = self.deviation_input.value()
        sig_formula = self.signal_plot.generate_formula_freqmod(signal_fs, signal_ss, freq_dev)
        self.signal_plot.axes.set_title(sig_formula)
        self.specter_plot.axes.set_title(self.specter_plot.generate_formula_spectr(row_formula=sig_formula))
        self.signal_plot.freq_modulate(signal_fs[2], self.x_scale_value, signal_ss[1], signal_ss[2], 
        signal_fs[1], self.y_scale_value, freq_dev)
        self.specter_plot.freq_modulate(signal_fs[2], signal_ss[2], freq_dev)
    
    def slider_frequency_move(self):

        if self.mechanical_slider_frequency.value() % 2 == 0:
            self.x_scale_value = 0.0011 * 10**(self.mechanical_slider_frequency.value() // 2)
        else:
            self.x_scale_value = 0.0055 * 10**(self.mechanical_slider_frequency.value() // 2)

        if self.mechanical_slider_amplitude.value() % 2 == 0:
            self.y_scale_value = 0.0011 * 10**(self.mechanical_slider_amplitude.value() // 2)
        else:
            self.y_scale_value = 0.0055 * 10**(self.mechanical_slider_amplitude.value() // 2)

        self.signal_plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)
        self.signal_plot.axes.set_xlim(-self.x_scale_value, self.x_scale_value)        

        self.signal_plot.view.draw()
        self.signal_plot.view.flush_events()

    def show_parametrs_button(self):
        if self.fs_signals_list.currentIndex() == -1 and self.ss_signals_list.currentIndex() == -1:
             return 

        ind_fs = self.fs_signals_list.currentIndex()
        ind_ss = self.ss_signals_list.currentIndex()
        signal_fs = self.signalDataArray.getSignalByIndex(ind_fs).getData()
        signal_ss = self.signalDataArray.getSignalByIndex(ind_ss).getData()

        M = round(signal_ss[1] / signal_fs[1], 2)

        formula = '\nM = Uм / Uн = ' + str(M) + '\n'

        self.parametr_window.show_parametrs(formula)

        self.parametr_window.show()

    def closeEvent(self, event):
        self.specter_plot.clear()
        self.signal_plot.clear()
        self.fs_signals_list.setCurrentIndex(1)
        self.ss_signals_list.setCurrentIndex(1)
        self.showSignalInfo_fs()
        self.showSignalInfo_ss()
        print("Frequency modulation window closed")