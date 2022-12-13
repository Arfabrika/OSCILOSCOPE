from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QCheckBox,
    QDial
)

from SignalPlotWidget import SignalPlotWidget
from signalData import signalData, signalDataArray

class SummationWindow(QWidget):
    def __init__(self, DataArray, animation_flag = 1, parent=None):
        super().__init__(parent)
        self.signalDataArray = DataArray
        self.animation_flag = animation_flag
        self.signalsOnPlot = signalDataArray([])
        
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

        self.fs_duration_spin = QLabel()
        self.fs_duration_label = QLabel('Продолжительность')
        self.fs_duration_label.setBuddy(self.fs_duration_spin)

        fs_duration_layout = QHBoxLayout()
        fs_duration_layout.addWidget(self.fs_duration_label)
        fs_duration_layout.addWidget(self.fs_duration_spin)


        fs_signal = QVBoxLayout()
        fs_signal.addLayout(fs_signals_layout)
        fs_signal.addLayout(fs_signals_form_layout)
        fs_signal.addLayout(fs_frequency_layout)
        fs_signal.addLayout(fs_amplitude_layout)
        fs_signal.addLayout(fs_duration_layout)

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
        self.mechanical_slider_amplitude.setRange(0, 50)
        self.mechanical_slider_amplitude.setValue(1)
        mechanical_slider_amplitude_layout.addWidget(self.amplitude_lable)
        mechanical_slider_amplitude_layout.addWidget(self.mechanical_slider_amplitude)
        self.mechanical_slider_amplitude.valueChanged.connect(self.slider_frequency_move)
        self.mechanical_slider_amplitude_checkbox = QCheckBox("Enabled")
        self.mechanical_slider_amplitude_checkbox.setChecked(True)
        mechanical_slider_amplitude_layout.addWidget(self.mechanical_slider_amplitude_checkbox)        
        
        mechanical_slider_frequency_layout = QVBoxLayout()
        self.frequency_lable = QLabel("ось x")
        self.mechanical_slider_frequency = QDial()
        self.mechanical_slider_frequency.setRange(0, 50)
        self.mechanical_slider_frequency.setValue(1)
        mechanical_slider_frequency_layout.addWidget(self.frequency_lable)
        mechanical_slider_frequency_layout.addWidget(self.mechanical_slider_frequency)
        self.mechanical_slider_frequency.valueChanged.connect(self.slider_frequency_move)
        self.mechanical_slider_frequency_checkbox = QCheckBox("Enabled")
        self.mechanical_slider_frequency_checkbox.setChecked(True)
        mechanical_slider_frequency_layout.addWidget(self.mechanical_slider_frequency_checkbox)

        mechanical_sliders = QVBoxLayout()
        mechanical_sliders.addLayout(mechanical_slider_frequency_layout)
        mechanical_sliders.addLayout(mechanical_slider_amplitude_layout)

        tmp = QHBoxLayout()
        tmp.addLayout(mechanical_sliders)

        plot_layout = QHBoxLayout()
        plot_layout.addLayout(tmp)
        plot_layout.addWidget(self.plot)

        main_layout.addLayout(signal_layout)
        main_layout.addWidget(self.ok_button)
        main_layout.addWidget(self.step_out_button)
        main_layout.addLayout(plot_layout)

        self.setLayout(main_layout)
        self.setSignals()

    def editScale(self):
        self.x_scale_value = float(self.scale_x.currentText())* 1.1
        self.y_scale_value = float(self.scale_y.currentText())* 1.1

        self.plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)
        self.plot.axes.set_xlim(-self.x_scale_value, self.x_scale_value)

        self.button_clicked()

    def updateSignalData(self, signalDataArray, animation_flag):
        self.signalDataArray = signalDataArray
        self.animation_flag = animation_flag
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
            self.plot.plot(curSignal_fs[0], curSignal_fs[2], curSignal_fs[1], 1, animation_flag=self.animation_flag)
            self.signalsOnPlot.appendSignal(signalData(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], False))
        elif self.signalsOnPlot.getArraySize() == 1:
            ss_signal = self.signalsOnPlot.getSignalByIndex(self.signalsOnPlot.getArraySize() - 1)
            self.plot.polyharmonic(curSignal_fs[0], curSignal_fs[2], curSignal_fs[1],
                     ss_signal.getSignaType(), ss_signal.getAmplitude(), ss_signal.getFrequency(), ss_signal.getDuration(), animation_flag=self.animation_flag)
            self.signalsOnPlot.appendSignal(signalData(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], False))
        else:
            self.plot.polyharmonic(curSignal_fs[0], curSignal_fs[2], curSignal_fs[1], animation_flag=self.animation_flag)
    
    def showSignalInfo_fs(self):
        if (self.signalDataArray.getArraySize() > 0):
            curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData() 

            self.fs_amplitude_spin.setText(str(curSignal_fs[1]))
            self.fs_duration_spin.setText(str(curSignal_fs[3]))
            self.fs_frequency_spin.setText(str(curSignal_fs[2]))
            self.fs_signal_form_combo.setText(curSignal_fs[0])
    
    def step_back(self):
        lastSigData = self.signalsOnPlot.getLastSignal().getData()
        
        if lastSigData[1] == 0 or self.signalsOnPlot.getArraySize() == 1:
            self.signalsOnPlot.clear()
            self.plot.clear()
            return
        
        self.plot.remove_last_points(lastSigData[6], lastSigData[7])
        self.signalsOnPlot.removeLast()

    def slider_frequency_move(self):

        self.x_scale_value = float(self.mechanical_slider_frequency.value())* 1.1
        self.y_scale_value = float(self.mechanical_slider_amplitude.value())* 1.1
        self.update_plot()

        self.signal_plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)
        self.signal_plot.axes.set_xlim(-self.x_scale_value, self.x_scale_value)

        self.signal_plot.view.draw()
        self.signal_plot.view.flush_events()


    def update_plot(self):
        ind_fs = self.fs_signals_list.currentIndex()
        ind_ss = self.ss_signals_list.currentIndex()
        signal_fs = self.signalDataArray.getSignalByIndex(ind_fs).getData()
        signal_ss = self.signalDataArray.getSignalByIndex(ind_ss).getData()
        self.signal_plot.modulate(signal_fs[2], signal_fs[3], self.mechanical_slider_frequency.value(), signal_ss[1], signal_ss[2], signal_fs[1], flag = 0, animation_flag=self.animation_flag)

       #bashkoff


