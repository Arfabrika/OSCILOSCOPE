from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)

from SignalPlotWidget import SignalPlotWidget
from signalData import signalData, signalDataArray

class SummationWindow(QWidget):
    def __init__(self, DataArray, parent=None):
        super().__init__(parent)
        self.signalDataArray = DataArray
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
        self.fs_signal_form_combo_label = QLabel('Signal form', self)
        self.fs_signal_form_combo_label.setBuddy(self.fs_signal_form_combo)

        fs_signals_form_layout = QHBoxLayout()
        fs_signals_form_layout.addWidget(self.fs_signal_form_combo_label)
        fs_signals_form_layout.addWidget(self.fs_signal_form_combo)

        self.fs_frequency_spin = QLabel()
        self.fs_frequency_label = QLabel('Frequency')
        self.fs_frequency_label.setBuddy(self.fs_frequency_spin)

        fs_frequency_layout = QHBoxLayout()
        fs_frequency_layout.addWidget(self.fs_frequency_label)
        fs_frequency_layout.addWidget(self.fs_frequency_spin)

        self.fs_amplitude_spin = QLabel()
        self.fs_amplitude_label = QLabel('Amplitude')
        self.fs_amplitude_label.setBuddy(self.fs_amplitude_spin)

        fs_amplitude_layout = QHBoxLayout()
        fs_amplitude_layout.addWidget(self.fs_amplitude_label)
        fs_amplitude_layout.addWidget(self.fs_amplitude_spin)

        self.fs_sample_rate_spin = QLabel()
        self.fs_sample_rate_label = QLabel('Sample rate, Hz')
        self.fs_sample_rate_label.setBuddy(self.fs_sample_rate_spin)

        fs_sample_rate_layout = QHBoxLayout()
        fs_sample_rate_layout.addWidget(self.fs_sample_rate_label)
        fs_sample_rate_layout.addWidget(self.fs_sample_rate_spin)

        self.fs_duration_spin = QLabel()
        self.fs_duration_label = QLabel('Duration, sec')
        self.fs_duration_label.setBuddy(self.fs_duration_spin)

        fs_duration_layout = QHBoxLayout()
        fs_duration_layout.addWidget(self.fs_duration_label)
        fs_duration_layout.addWidget(self.fs_duration_spin)


        fs_signal = QVBoxLayout()
        fs_signal.addLayout(fs_signals_layout)
        fs_signal.addLayout(fs_signals_form_layout)
        fs_signal.addLayout(fs_frequency_layout)
        fs_signal.addLayout(fs_amplitude_layout)
        fs_signal.addLayout(fs_sample_rate_layout)
        fs_signal.addLayout(fs_duration_layout)

        self.ok_button = QPushButton('Add signal')
        self.ok_button.clicked.connect(self.button_clicked)
        self.step_out_button = QPushButton('Step back')
        self.step_out_button.clicked.connect(self.step_back)

        self.plot = SignalPlotWidget()

        signal_layout = QHBoxLayout()

        signal_layout.addLayout(fs_signal)

        main_layout = QVBoxLayout()

        main_layout.addLayout(signal_layout)
        main_layout.addWidget(self.ok_button)
        main_layout.addWidget(self.step_out_button)
        main_layout.addWidget(self.plot)

        self.setLayout(main_layout)
        self.setSignals()

    def setSignals(self):
        data = self.signalDataArray.getArray()
        if len(data) == 0:
            self.fs_signals_list.addItem("No signals")
        else:
            for i in range(len(data)):
                self.fs_signals_list.addItem('Signal ' + str(i + 1))

    
    def button_clicked(self):
        curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData() 
       
        if self.signalsOnPlot.getArraySize() == 0:
            self.plot.plot(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], curSignal_fs[3], curSignal_fs[4], 1, 1)
            self.signalsOnPlot.appendSignal(signalData(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], curSignal_fs[3], curSignal_fs[4], False))
        elif self.signalsOnPlot.getArraySize() == 1:
            ss_signal = self.signalsOnPlot.getSignalByIndex(self.signalsOnPlot.getArraySize() - 1)
            self.plot.polyharmonic(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], curSignal_fs[3], curSignal_fs[4], ss_signal.getSignaType(), ss_signal.getAmplitude(), ss_signal.getFrequency(), ss_signal.getSampleRate(), ss_signal.getDuration())
            self.signalsOnPlot.appendSignal(signalData(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], curSignal_fs[3], curSignal_fs[4], False))
        else:
            self.plot.polyharmonic(curSignal_fs[0], curSignal_fs[1], curSignal_fs[2], curSignal_fs[3], curSignal_fs[4])
    
    def showSignalInfo_fs(self):
       curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData() 

       self.fs_amplitude_spin.setText(str(curSignal_fs[1]))
       self.fs_duration_spin.setText(str(curSignal_fs[4]))
       self.fs_frequency_spin.setText(str(curSignal_fs[2]))
       self.fs_sample_rate_spin.setText(str(curSignal_fs[3]))
       self.fs_signal_form_combo.setText(curSignal_fs[0])
    
    def step_back(self):
        self.plot.remove_last_points()
       # bashkoff


