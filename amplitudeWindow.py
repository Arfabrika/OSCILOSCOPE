from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout
)

class AmplitudeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.fs_signals_label = QLabel('Основной сигнал')
        self.fs_signals_list = QComboBox(self)
        #self.signals_list.addItems(signal_types)
        self.fs_signals_label.setBuddy(self.fs_signals_list)

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

        main_window = QHBoxLayout()

        main_window.addLayout(fs_signal)
        main_window.addLayout(ss_signal)

        self.setLayout(main_window)
