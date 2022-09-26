import sys
import struct

from PySide6.QtCore import QThreadPool

from PySide6.QtWidgets import (
    QErrorMessage,
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLabel,
    QSpinBox,
    QPushButton,
    QMessageBox
)

from SignalPlotWidget import SignalPlotWidget
from SpectrePlotWidget import SpectrePlotWidget

import serial.tools.list_ports


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.thread_manager = QThreadPool()
        
        self.stop_flag = False

        
        self.serial_ports_combo = QComboBox(self)
        self.serial_ports = serial.tools.list_ports.comports()
        serial_ports_desc = [port.name for port in self.serial_ports]
        serial_ports_desc.reverse()
        # serial_ports_desc.insert(0, '-')
        self.serial_ports_combo.addItems(serial_ports_desc)
        self.serial_ports_combo_label = QLabel('Select port', self)
        self.serial_ports_combo_label.setBuddy(self.serial_ports_combo)
        
        
        
        self.amplitude_sensitivity_label = QLabel('Amplitude sensitivity', self)
        self.amplitude_sensitivity_spin = QSpinBox()
        self.amplitude_sensitivity_spin.setRange(0, 200_000)
        self.amplitude_sensitivity_spin.setValue(1)
        self.amplitude_sensitivity_label.setBuddy(self.amplitude_sensitivity_spin)

        self.fs_params_label = QLabel('First signal', self)
        self.fs_toggle_button = QPushButton('ON/OFF', self)
        self.fs_toggle_button.setCheckable(True)
        self.fs_toggle_button.clicked.connect(self.set_signal)
        self.fs_params_label.setBuddy(self.fs_toggle_button)

        signal_types = ['-', 'sine', 'cosine', 'triangle', 'sawtooth', 'square']

        self.fs_signal_form_combo = QComboBox(self)
        self.fs_signal_form_combo.addItems(signal_types)
        self.fs_signal_form_combo_label = QLabel('Signal form', self)
        self.fs_signal_form_combo_label.setBuddy(self.fs_signal_form_combo)

        self.signal_plot = SignalPlotWidget()
        self.spectre_plot = SpectrePlotWidget()

        self.fs_frequency_spin = QSpinBox()
        self.fs_frequency_spin.setRange(0, 200_000)
        self.fs_frequency_spin.setValue(1)
        self.fs_frequency_label = QLabel('Frequency')
        self.fs_frequency_label.setBuddy(self.fs_frequency_spin)

        self.fs_amplitude_spin = QSpinBox()
        self.fs_amplitude_spin.setRange(0, 200_000)
        self.fs_amplitude_spin.setValue(1)
        self.fs_amplitude_label = QLabel('Amplitude')
        self.fs_amplitude_label.setBuddy(self.fs_amplitude_spin)

        unit_prefixes = ["Hz", "kHz", "mHz", "nHz"]

        self.unit_prefixes_Hz = QComboBox(self)
        self.unit_prefixes_Hz.addItems(unit_prefixes)
        self.unit_prefixes_Hz.setFixedWidth(50)

        self.hiden_widh_1 = QLabel(self)
        self.hiden_widh_1.setFixedWidth(343)

        self.fs_sample_rate_spin = QSpinBox()
        self.fs_sample_rate_spin.setRange(0, 200_000)
        self.fs_sample_rate_spin.setValue(440)
        self.fs_sample_rate_spin.setFixedWidth(470)
        self.fs_sample_rate_label = QLabel('Sample rate')
        self.fs_sample_rate_label.setFixedWidth(65)
        self.fs_sample_rate_label.setBuddy(self.fs_sample_rate_spin)

        unit_prefixes_sec = ["sec", "msec",]
        self.unit_prefixes_sec = QComboBox(self)
        self.unit_prefixes_sec.addItems(unit_prefixes_sec)
        self.unit_prefixes_sec.setFixedWidth(60)

        self.fs_duration_spin = QSpinBox()
        self.fs_duration_spin.setValue(5)
        self.fs_duration_spin.setFixedWidth(470)
        self.fs_duration_label = QLabel('Duration')
        self.fs_duration_label.setBuddy(self.fs_duration_spin)
        
        serial_ports_layout = QHBoxLayout()
        serial_ports_layout.addWidget(self.serial_ports_combo_label)
        serial_ports_layout.addWidget(self.serial_ports_combo)
        
        amplitude_sensitivity_layout = QHBoxLayout()
        amplitude_sensitivity_layout.addWidget(self.amplitude_sensitivity_label)
        amplitude_sensitivity_layout.addWidget(self.amplitude_sensitivity_spin)

        fs_params_layout = QVBoxLayout()

        fs_switch_layout = QHBoxLayout()
        fs_switch_layout.addWidget(self.fs_params_label)
        fs_switch_layout.addWidget(self.fs_toggle_button)

        fs_signal_form_layout = QHBoxLayout()
        fs_signal_form_layout.addWidget(self.fs_signal_form_combo_label)
        fs_signal_form_layout.addWidget(self.fs_signal_form_combo)

        fs_frequency_input_layout = QHBoxLayout()
        fs_frequency_input_layout.addWidget(self.fs_frequency_label)
        fs_frequency_input_layout.addWidget(self.fs_frequency_spin)

        fs_amplitude_input_layout = QHBoxLayout()
        fs_amplitude_input_layout.addWidget(self.fs_amplitude_label)
        fs_amplitude_input_layout.addWidget(self.fs_amplitude_spin)

        fs_sample_rate_input_layout = QHBoxLayout()
        fs_sample_rate_input_layout.addWidget(self.fs_sample_rate_label)
        fs_sample_rate_input_layout.addWidget(self.unit_prefixes_Hz)
        fs_sample_rate_input_layout.addWidget(self.hiden_widh_1)
        fs_sample_rate_input_layout.addWidget(self.fs_sample_rate_spin)

        fs_duration_input_layout = QHBoxLayout()
        fs_duration_input_layout.addWidget(self.fs_duration_label)
        fs_duration_input_layout.addWidget(self.unit_prefixes_sec)
        fs_duration_input_layout.addWidget(self.hiden_widh_1)
        fs_duration_input_layout.addWidget(self.fs_duration_spin)


        fs_params_layout.addLayout(fs_switch_layout)
        fs_params_layout.addLayout(fs_signal_form_layout)
        fs_params_layout.addLayout(fs_frequency_input_layout)
        fs_params_layout.addLayout(fs_amplitude_input_layout)
        fs_params_layout.addLayout(fs_sample_rate_input_layout)
        fs_params_layout.addLayout(fs_duration_input_layout)

        self.ss_params_label = QLabel('Second signal')
        self.ss_toggle_button = QPushButton('ON/OFF', self)
        self.ss_toggle_button.setCheckable(True)
        self.ss_toggle_button.clicked.connect(self.set_signal)
        self.ss_params_label.setBuddy(self.ss_toggle_button)
        
        self.ss_signal_form_combo_label = QLabel('Signal form', self)
        self.ss_signal_form_combo = QComboBox(self)
        self.ss_signal_form_combo.addItems(signal_types)
        self.ss_signal_form_combo_label.setBuddy(self.ss_signal_form_combo)

        self.ss_frequency_spin = QSpinBox()
        self.ss_frequency_spin.setRange(0, 200_000)
        self.ss_frequency_spin.setValue(1)
        self.ss_frequency_label = QLabel('Frequency')
        self.ss_frequency_label.setBuddy(self.ss_frequency_spin)

        self.ss_amplitude_spin = QSpinBox()
        self.ss_amplitude_spin.setRange(0, 200_000)
        self.ss_amplitude_spin.setValue(1)
        self.ss_amplitude_label = QLabel('Amplitude')
        self.ss_amplitude_label.setBuddy(self.ss_amplitude_spin)

        self.ss_sample_rate_spin = QSpinBox()
        self.ss_sample_rate_spin.setRange(0, 200_000)
        self.ss_sample_rate_spin.setValue(440)
        self.ss_sample_rate_label = QLabel('Sample rate, Hz')
        self.ss_sample_rate_label.setBuddy(self.ss_sample_rate_spin)

        self.ss_duration_spin = QSpinBox()
        self.ss_duration_spin.setValue(5)
        self.ss_duration_label = QLabel('Duration, sec')
        self.ss_duration_label.setBuddy(self.ss_duration_spin)

        ss_params_layout = QVBoxLayout()

        ss_switch_layout = QHBoxLayout()
        ss_switch_layout.addWidget(self.ss_params_label)
        ss_switch_layout.addWidget(self.ss_toggle_button)

        ss_signal_form_layout = QHBoxLayout()
        ss_signal_form_layout.addWidget(self.ss_signal_form_combo_label)
        ss_signal_form_layout.addWidget(self.ss_signal_form_combo)

        ss_frequency_input_layout = QHBoxLayout()
        ss_frequency_input_layout.addWidget(self.ss_frequency_label)
        ss_frequency_input_layout.addWidget(self.ss_frequency_spin)

        ss_amplitude_input_layout = QHBoxLayout()
        ss_amplitude_input_layout.addWidget(self.ss_amplitude_label)
        ss_amplitude_input_layout.addWidget(self.ss_amplitude_spin)

        ss_sample_rate_input_layout = QHBoxLayout()
        ss_sample_rate_input_layout.addWidget(self.ss_sample_rate_label)
        ss_sample_rate_input_layout.addWidget(self.ss_sample_rate_spin)

        ss_duration_input_layout = QHBoxLayout()
        ss_duration_input_layout.addWidget(self.ss_duration_label)
        ss_duration_input_layout.addWidget(self.ss_duration_spin)

        ss_params_layout.addLayout(ss_switch_layout)
        ss_params_layout.addLayout(ss_signal_form_layout)
        ss_params_layout.addLayout(ss_frequency_input_layout)
        ss_params_layout.addLayout(ss_amplitude_input_layout)
        ss_params_layout.addLayout(ss_sample_rate_input_layout)
        ss_params_layout.addLayout(ss_duration_input_layout)

        params_layout = QHBoxLayout()
        params_layout.addLayout(fs_params_layout)
        params_layout.addLayout(ss_params_layout)

        plots_layout = QHBoxLayout()
        plots_layout.addWidget(self.signal_plot)
        plots_layout.addWidget(self.spectre_plot)

        self.com_error_message = QErrorMessage()
        self.receive_button = QPushButton('Receive')
        self.stop_listening_button = QPushButton('Stop')

        main_layout = QVBoxLayout()
        main_layout.addLayout(serial_ports_layout)
        main_layout.addLayout(amplitude_sensitivity_layout)
        main_layout.addLayout(params_layout)
        main_layout.addLayout(plots_layout)
        main_layout.addWidget(self.receive_button)
        main_layout.addWidget(self.stop_listening_button)

        self.setLayout(main_layout)

        self.receive_button.clicked.connect(self.receive_signal_safely)
        self.stop_listening_button.clicked.connect(self.set_stop_safely)

        self.showMaximized()
        
    
    def set_stop(self):
        print('set stop')
        self.stop_flag = True

    def set_stop_safely(self):
        self.thread_manager.start(self.set_stop)
    
    
    def receive_signal(self):
        if self.serial_ports_combo.currentText() == '-':
            return
            
        else:
            self.stop_flag = False
            generator_name = self.serial_ports_combo.currentText()
            print(generator_name)

            for port in self.serial_ports:
                if generator_name == port.name:
                    print("Found serial port")
                    if 'serial' in port.description.lower() or 'VCP' in port.description.lower():
                        # init serial port and bound
                        # bound rate on two ports must be the same
                        generator_ser = serial.Serial(generator_name, 9600, timeout=1)
                        generator_ser.flushInput()
                        print(generator_ser.portstr)

                        data = []

                        print('stop flag', self.stop_flag)

                        while not self.stop_flag: # чтение байтов с порта                          
                            ser_bytes = generator_ser.readline()
                            print('huint', ser_bytes, len(ser_bytes) )
                            if len(ser_bytes) != 0:
                                try:
                                    for i in range(0, len(ser_bytes)-1, 2):
                                        data.append(int.from_bytes(ser_bytes[i:i+2], 'little'))
                                    print(ser_bytes)
                                except:
                                    print('error')
                        else:
                            print("Stop flag:", self.stop_flag)
                            print("Data", data)
                            self.signal_plot.clear()
                            self.spectre_plot.clear()
                            self.spectre_plot.axes.magnitude_spectrum(data, color='#1f77b4')
                            self.signal_plot.axes.plot(data, color='#1f77b4')
                            self.signal_plot.view.draw()
                            return
                    else:
                        self.com_error_message.showMessage("К данному порту не подключено серийное устройство")
                        return
                        

    def receive_signal_safely(self):
        self.thread_manager.start(self.receive_signal)
    
    def set_signal(self):
        if not (self.fs_toggle_button.isChecked() or self.ss_toggle_button.isChecked()):
            self.signal_plot.clear()
            self.spectre_plot.clear()
            return

        amplitude_sensitivity = self.amplitude_sensitivity_spin.value()

        fs_form_name = self.fs_signal_form_combo.currentText()
        fs_amplitude = self.fs_amplitude_spin.value()
        fs_frequency = self.fs_frequency_spin.value()
        fs_sample_rate = self.fs_sample_rate_spin.value()
        fs_duration = self.fs_duration_spin.value()

        ss_form_name = self.ss_signal_form_combo.currentText()
        ss_amplitude = self.ss_amplitude_spin.value()
        ss_frequency = self.ss_frequency_spin.value()
        ss_sample_rate = self.ss_sample_rate_spin.value()
        ss_duration = self.ss_duration_spin.value()
        
        if self.fs_toggle_button.isChecked() and self.ss_toggle_button.isChecked():
            self.signal_plot.modulate(amplitude_sensitivity, fs_form_name, fs_frequency, fs_sample_rate,
            fs_duration, ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
            
            self.spectre_plot.modulate(amplitude_sensitivity, fs_form_name, fs_frequency, fs_sample_rate, fs_duration,
                                       ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)


            # self.signal_plot.polyharmonic(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
            #                               ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
            # self.spectre_plot.polyharmonic(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
            #                                ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
        elif self.ss_toggle_button.isChecked():
            self.signal_plot.plot(ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
            self.spectre_plot.plot(ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
            
        elif self.fs_toggle_button.isChecked():
            self.signal_plot.plot(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration)
            self.spectre_plot.plot(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration)



        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
