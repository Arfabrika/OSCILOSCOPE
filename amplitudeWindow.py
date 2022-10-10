from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)

class AmplitudeWindow(QWidget):
    def __init__(self, signalDataArray, parent=None):
        super().__init__(parent)
        self.signalDataArray = signalDataArray
        
        self.fs_signals_label = QLabel('Основной сигнал')
        self.fs_signals_list = QComboBox(self)
        #self.signals_list.addItems(signal_types)
        self.fs_signals_label.setBuddy(self.fs_signals_list)
        self.fs_signals_list.currentIndexChanged.connect(self.showSignalInfo_fs)

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

        self.ss_signals_label = QLabel('Модулирующий сигнал')
        self.ss_signals_list = QComboBox(self)
        #self.signals_list.addItems(signal_types)
        self.ss_signals_label.setBuddy(self.ss_signals_list)
        self.ss_signals_list.currentIndexChanged.connect(self.showSignalInfo_ss)

        ss_signals_layout = QHBoxLayout()
        ss_signals_layout.addWidget(self.ss_signals_label)
        ss_signals_layout.addWidget(self.ss_signals_list)

        self.ss_signal_form_combo = QLabel(self)
        self.ss_signal_form_combo_label = QLabel('Signal form', self)
        self.ss_signal_form_combo_label.setBuddy(self.ss_signal_form_combo)

        ss_signals_form_layout = QHBoxLayout()
        ss_signals_form_layout.addWidget(self.ss_signal_form_combo_label)
        ss_signals_form_layout.addWidget(self.ss_signal_form_combo)

        self.ss_frequency_spin = QLabel()
        self.ss_frequency_label = QLabel('Frequency')
        self.ss_frequency_label.setBuddy(self.ss_frequency_spin)

        ss_frequency_layout = QHBoxLayout()
        ss_frequency_layout.addWidget(self.ss_frequency_label)
        ss_frequency_layout.addWidget(self.ss_frequency_spin)

        self.ss_amplitude_spin = QLabel()
        self.ss_amplitude_label = QLabel('Amplitude')
        self.ss_amplitude_label.setBuddy(self.ss_amplitude_spin)

        ss_amplitude_layout = QHBoxLayout()
        ss_amplitude_layout.addWidget(self.ss_amplitude_label)
        ss_amplitude_layout.addWidget(self.ss_amplitude_spin)

        self.ss_sample_rate_spin = QLabel()
        self.ss_sample_rate_label = QLabel('Sample rate, Hz')
        self.ss_sample_rate_label.setBuddy(self.ss_sample_rate_spin)

        ss_sample_rate_layout = QHBoxLayout()
        ss_sample_rate_layout.addWidget(self.ss_sample_rate_label)
        ss_sample_rate_layout.addWidget(self.ss_sample_rate_spin)

        self.ss_duration_spin = QLabel()
        self.ss_duration_label = QLabel('Duration, sec')
        self.ss_duration_label.setBuddy(self.ss_duration_spin)

        ss_duration_layout = QHBoxLayout()
        ss_duration_layout.addWidget(self.ss_duration_label)
        ss_duration_layout.addWidget(self.ss_duration_spin)

        ss_signal = QVBoxLayout()
        ss_signal.addLayout(ss_signals_layout)
        ss_signal.addLayout(ss_signals_form_layout)
        ss_signal.addLayout(ss_frequency_layout)
        ss_signal.addLayout(ss_amplitude_layout)
        ss_signal.addLayout(ss_sample_rate_layout)
        ss_signal.addLayout(ss_duration_layout)

        self.ok_button = QPushButton('Create plots')
        #self.ok_button.clicked.connect(self.ok_button_clicked)

        signal_layout = QHBoxLayout()

        signal_layout.addLayout(fs_signal)
        signal_layout.addLayout(ss_signal)

        main_layout = QVBoxLayout()

        main_layout.addLayout(signal_layout)
        main_layout.addWidget(self.ok_button)

        self.setLayout(main_layout)
        self.setSignals()

    def setSignals(self):
        data = self.signalDataArray.getArray()
        if len(data) == 0:
            self.fs_signals_list.addItem("No signals")
            self.ss_signals_list.addItem("No signals")
        else:
            for i in range(len(data)):
                self.fs_signals_list.addItem('Signal ' + str(i + 1))
                self.ss_signals_list.addItem('Signal ' + str(i + 1))

    def showSignalInfo_fs(self):
       curSignal_fs = self.signalDataArray.getSignalByIndex(self.fs_signals_list.currentIndex()).getData() 

       self.fs_amplitude_spin.setText(str(curSignal_fs[1]))
       self.fs_duration_spin.setText(str(curSignal_fs[4]))
       self.fs_frequency_spin.setText(str(curSignal_fs[2]))
       self.fs_sample_rate_spin.setText(str(curSignal_fs[3]))
       self.fs_signal_form_combo.setText(curSignal_fs[0])

    def showSignalInfo_ss(self):
       curSignal_ss = self.signalDataArray.getSignalByIndex(self.ss_signals_list.currentIndex()).getData() 

       self.ss_amplitude_spin.setText(str(curSignal_ss[1]))
       self.ss_duration_spin.setText(str(curSignal_ss[4]))
       self.ss_frequency_spin.setText(str(curSignal_ss[2]))
       self.ss_sample_rate_spin.setText(str(curSignal_ss[3]))
       self.ss_signal_form_combo.setText(curSignal_ss[0])

    def getSignal_ss(self):
        return self.ss_signals_list.currentIndex()

    def getSignal_fs(self):
        return self.fs_signals_list.currentIndex()
    """
    def ok_button_clicked(self):
        print("Ok clicked")
        self.parent().signals_label.setText("AAA")
    """



