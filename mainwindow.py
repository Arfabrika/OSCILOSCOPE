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
    QPushButton
)

from SignalPlotWidget import SignalPlotWidget
from SpectrePlotWidget import SpectrePlotWidget
from amplitudeWindow import AmplitudeWindow
from signalData import signalData, signalDataArray

import serial.tools.list_ports

from summationWindow import SummationWindow

signal_types = ['-', 'sine', 'cosine', 'triangle', 'sawtooth', 'square']

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.thread_manager = QThreadPool()
        
        self.stop_flag = False

        self.signalDataArray = signalDataArray([])

        self.amplitude_window = None

        self.summation_window = None
        
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
        
        active_label_layout = QHBoxLayout()
        active_label_layout.setDirection(QHBoxLayout.RightToLeft)
        self.active_label = QLabel('Choose signal', self)
        #self.active_label = QLabel('a', self) крип, крипочек
        active_label_layout.addWidget(self.active_label)

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

        self.fs_sample_rate_spin = QSpinBox()
        self.fs_sample_rate_spin.setRange(0, 200_000)
        self.fs_sample_rate_spin.setValue(440)
        self.fs_sample_rate_label = QLabel('Sample rate, Hz')
        self.fs_sample_rate_label.setBuddy(self.fs_sample_rate_spin)

        self.fs_duration_spin = QSpinBox()
        self.fs_duration_spin.setValue(5)
        self.fs_duration_label = QLabel('Duration, sec')
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
        #fs_switch_layout.addWidget(self.active_label)

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
        fs_sample_rate_input_layout.addWidget(self.fs_sample_rate_spin)

        fs_duration_input_layout = QHBoxLayout()
        fs_duration_input_layout.addWidget(self.fs_duration_label)
        fs_duration_input_layout.addWidget(self.fs_duration_spin)

        fs_signal_buttons_input_layout = QHBoxLayout()
        self.add_signal_button = QPushButton('Add signal', self)
        self.edit_signal_button = QPushButton('Edit current signal', self)
        fs_signal_buttons_input_layout.addWidget(self.add_signal_button)
        fs_signal_buttons_input_layout.addWidget(self.edit_signal_button)

        
        fs_params_layout.addLayout(fs_switch_layout)
        fs_params_layout.addLayout(active_label_layout)
        #fs_params_layout.addWidget(self.active_label)
        fs_params_layout.addLayout(fs_signal_form_layout)
        fs_params_layout.addLayout(fs_frequency_input_layout)
        fs_params_layout.addLayout(fs_amplitude_input_layout)
        fs_params_layout.addLayout(fs_sample_rate_input_layout)
        fs_params_layout.addLayout(fs_duration_input_layout)
        fs_params_layout.addLayout(fs_signal_buttons_input_layout)

        """
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
        """
       
        self.signals_label = QLabel('Список сигналов')
        self.signals_list = QComboBox(self)
        #self.signals_list.addItems(signal_types)
        self.signals_label.setBuddy(self.signals_list)

        signals_list_layout = QHBoxLayout()
        signals_list_layout.addWidget(self.signals_label)
        signals_list_layout.addWidget(self.signals_list)
        
        ampl_layout = QVBoxLayout()
        self.ampl_create_button = QPushButton('Create amplitude modulation')
        self.ampl_create_button.setCheckable(True)
        self.ampl_create_button.clicked.connect(self.click_amplitude_event)
        self.sum_create_button = QPushButton('Create summation plots')
        self.sum_create_button.setCheckable(True)
        self.sum_create_button.clicked.connect(self.click_sum_event)
        ampl_layout.addLayout(signals_list_layout)
        ampl_layout.addWidget(self.ampl_create_button)
        ampl_layout.addWidget(self.sum_create_button)


        params_layout = QHBoxLayout()
        params_layout.addLayout(fs_params_layout)
        params_layout.addLayout(ampl_layout)
        #params_layout.addLayout(ss_params_layout)

        plot_params_layout = QVBoxLayout()
        plot_params_scale_x = QVBoxLayout()
        self.scale_x = QComboBox()
        self.scale_x.addItems(['0.001', '0.01', '0.1', '1', '10', '100', '1000'])
        self.scale_x.setCurrentIndex(3)
        self.scale_x_label = QLabel("Max x scale")

        plot_params_scale_x.addWidget(self.scale_x_label)
        plot_params_scale_x.addWidget(self.scale_x)

        plot_params_scale_y = QVBoxLayout()
        self.scale_y = QComboBox()
        self.scale_y.addItems(['0.001', '0.01', '0.1', '1', '10', '100', '1000'])
        self.scale_y.setCurrentIndex(3)
        self.scale_y_label = QLabel("Max y scale")

        plot_params_scale_y.addWidget(self.scale_y_label)
        plot_params_scale_y.addWidget(self.scale_y)

        plot_params_layout.addLayout(plot_params_scale_x)
        plot_params_layout.addLayout(plot_params_scale_y)
        plot_params_layout.addStretch()
        self.scale_x.currentIndexChanged.connect(self.editScale)
        self.scale_y.currentIndexChanged.connect(self.editScale)

        plots_layout = QHBoxLayout()
        plots_layout.addLayout(plot_params_layout)
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
        self.loadSignals()
        self.add_signal_button.clicked.connect(self.addSignal)
        self.receive_button.clicked.connect(self.receive_signal_safely)
        self.stop_listening_button.clicked.connect(self.set_stop_safely)
        self.signals_list.currentIndexChanged.connect(self.showSignals)
        self.edit_signal_button.clicked.connect(self.editSignal)
        #self.fs_toggle_button.clicked.connect(self.changeSignalActivity)
        self.x_scale_value = 1
        self.y_scale_value = 1

        self.showMaximized()

    def addSignal(self):
        form_name = self.fs_signal_form_combo.currentText()
        amplitude = self.fs_amplitude_spin.value()
        frequency = self.fs_frequency_spin.value()
        sample_rate = self.fs_sample_rate_spin.value()
        duration = self.fs_duration_spin.value()
        self.signalDataArray.appendSignal(signalData(form_name, amplitude, frequency, sample_rate, duration, False))
        self.loadSignals()
    
    def loadSignals(self):  
        self.signals_list.clear()      
        data = self.signalDataArray.getArray()
        if len(data) == 0:
            self.signals_list.addItem("New signal")
        else:
            for i in range(len(data)):
                self.signals_list.addItem('Signal ' + str(i + 1))
            self.signals_list.addItem('New signal')

    def editSignal(self):
        form_name = self.fs_signal_form_combo.currentText()
        amplitude = self.fs_amplitude_spin.value()
        frequency = self.fs_frequency_spin.value()
        sample_rate = self.fs_sample_rate_spin.value()
        duration = self.fs_duration_spin.value()
        curInd = self.signals_list.currentIndex()
        if ((curInd != self.signalDataArray.getArraySize()) 
        and (curInd != -1)):
            self.signalDataArray.editSignalByIndex(signalData(form_name, amplitude, frequency, sample_rate, duration), curInd)
            self.loadSignals()

    def changeSignalActivity(self):
        curInd = self.signals_list.currentIndex()
        if ((curInd != self.signalDataArray.getArraySize()) 
        and (curInd != -1)):
           self.signalDataArray.array[curInd].changeActivity() 
            
    
    def showSignals(self):
        if ((self.signals_list.currentIndex() == 0 and self.signalDataArray.getArraySize() == 0)
        or (self.signals_list.currentIndex() == self.signalDataArray.getArraySize())):
            self.fs_signal_form_combo.setCurrentIndex(1)
            self.fs_amplitude_spin.setValue(1)
            self.fs_duration_spin.setValue(5)
            self.fs_frequency_spin.setValue(1)
            self.fs_sample_rate_spin.setValue(440)
        elif self.signals_list.currentIndex() != -1:           
            curSignal = self.signalDataArray.getSignalByIndex(self.signals_list.currentIndex()).getData()
            self.fs_signal_form_combo.setCurrentIndex(signal_types.index(curSignal[0]))
            self.fs_amplitude_spin.setValue(curSignal[1])
            self.fs_duration_spin.setValue(curSignal[4])
            self.fs_frequency_spin.setValue(curSignal[2])
            self.fs_sample_rate_spin.setValue(curSignal[3]) 
            
            if curSignal[5] == True:
                self.active_label.setText("Signal is active") 
            else:
                self.active_label.setText("Signal is inactive")

    def editScale(self):
        self.x_scale_value = float(self.scale_x.currentText())
        self.y_scale_value = float(self.scale_y.currentText())
        self.signal_plot.clear()
        self.spectre_plot.clear()
        #self.signal_plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)

        if self.amplitude_window.isVisible():
            self.ok_button_clicked()
            print("in ampl")
        else:
            self.signalDataArray.array[self.signals_list.currentIndex()].changeActivity()
            self.set_signal()
            print("in common")
    
            
    
    def set_stop(self):
        #print('set stop')
        self.stop_flag = True

    def set_stop_safely(self):
        self.thread_manager.start(self.set_stop)
    
    
    def receive_signal(self):
        if self.serial_ports_combo.currentText() == '-':
            return
            
        else:
            self.stop_flag = False
            generator_name = self.serial_ports_combo.currentText()

            self.signal_plot.clear()
            self.spectre_plot.clear()

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

                        #print('stop flag', self.stop_flag)

                        while not self.stop_flag: # чтение байтов с порта                          
                            ser_bytes = generator_ser.read(4)
                            # print('huint', ser_bytes, len(ser_bytes) )
                            if len(ser_bytes) != 0:
                                try:
                                    data.append(struct.unpack('f', ser_bytes)[0])
                                    # print(ser_bytes)
                                except Exception as e:
                                    print('error', str(e))
                            self.signal_plot.axes.clear() # fixed
                            self.signal_plot.axes.grid(True)
                            self.spectre_plot.axes.magnitude_spectrum(data, color='#1f77b4')
                            
                            self.signal_plot.axes.plot(data, color='#1f77b4')
                            self.signal_plot.view.draw()
                            self.spectre_plot.view.draw()
                            

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

    def ok_button_clicked(self):
        ind_fs = self.amplitude_window.fs_signals_list.currentIndex()
        ind_ss = self.amplitude_window.ss_signals_list.currentIndex()
        signal_fs = self.signalDataArray.getSignalByIndex(ind_fs).getData()
        signal_ss = self.signalDataArray.getSignalByIndex(ind_ss).getData()
        self.signal_plot.modulate(signal_fs[2], signal_fs[3], self.x_scale_value, signal_ss[1], signal_ss[2], signal_fs[1], self.y_scale_value)
        self.spectre_plot.modulate(signal_fs[2], signal_fs[3], signal_fs[4], signal_ss[1], signal_ss[2], signal_fs[1])

    def click_amplitude_event(self):
        self.amplitude_window = AmplitudeWindow(self.signalDataArray)
        self.amplitude_window.show()
        self.amplitude_window.ok_button.clicked.connect(self.ok_button_clicked)
    
    def click_sum_event(self):
        self.summation_window = SummationWindow(self.signalDataArray)
        self.summation_window.show()
        self.summation_window.ok_button.clicked.connect(self.ok_button_clicked)

    def set_signal(self):
        if self.signalDataArray.getArraySize == 0:
            return
        self.signalDataArray.array[self.signals_list.currentIndex()].changeActivity()
        if self.signalDataArray.array[self.signals_list.currentIndex()].getActivity() == True:
            self.active_label.setText("Signal is active")
            """
            if not (self.fs_toggle_button.isChecked()):# or self.ss_toggle_button.isChecked()):
                self.signal_plot.clear()
                self.spectre_plot.clear()
                return
            """

            amplitude_sensitivity = self.amplitude_sensitivity_spin.value()

            fs_form_name = self.fs_signal_form_combo.currentText()
            fs_amplitude = self.fs_amplitude_spin.value()
            fs_frequency = self.fs_frequency_spin.value()
            fs_sample_rate = self.fs_sample_rate_spin.value()
            fs_duration = self.fs_duration_spin.value()
            """
            ss_form_name = self.ss_signal_form_combo.currentText()
            ss_amplitude = self.ss_amplitude_spin.value()
            ss_frequency = self.ss_frequency_spin.value()
            ss_sample_rate = self.ss_sample_rate_spin.value()
            ss_duration = self.ss_duration_spin.value()
            """
            """
            if self.fs_toggle_button.isChecked() and self.ss_toggle_button.isChecked():
                # self.signal_plot.modulate(amplitude_sensitivity, fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate,
                # fs_duration, ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
                # self.spectre_plot.modulate(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
                #                            ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
                self.signal_plot.polyharmonic(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
                                            ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
                self.spectre_plot.polyharmonic(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
                                            ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
            elif self.ss_toggle_button.isChecked():
                self.signal_plot.plot(ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
                self.spectre_plot.plot(ss_form_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)
            el"""   
        #if self.fs_toggle_button.isChecked():
            self.signal_plot.plot(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate,
             fs_duration, self.x_scale_value, self.y_scale_value)
            self.spectre_plot.plot(fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration)
        else:
            self.active_label.setText("Signal is inactive")

            #rewrite clear part
            self.signal_plot.clear()
            self.spectre_plot.clear()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


