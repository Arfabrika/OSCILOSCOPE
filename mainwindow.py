import sys
import struct
import numpy as np
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
    QDial,
    QCheckBox,
)

from PySide6.QtGui import QAction

from SignalPlotWidget import SignalPlotWidget
from SpectrePlotWidget import SpectrePlotWidget
from amplitudeWindow import AmplitudeWindow
from frequencyWindow import FrequencyWindow
from signalData import signalData, signalDataArray
from RealSingalWindow import RealSignalWindow

import serial.tools.list_ports
import time

from summationWindow import SummationWindow
signal_types = ['-', 'sine', 'cosine', 'triangle', 'sawtooth', 'square']
from functools import partial, wraps
from wave import (generate_data_spectrum)

class CoolDownDecorator(object):
  def __init__(self,func,interval):
    self.func = func
    self.interval = interval
    self.last_run = 0
  def __get__(self,obj,objtype=None):
    if obj is None:
      return self.func
    return partial(self,obj)
  def __call__(self,*args,**kwargs):
    now = time.time()
    if now - self.last_run > self.interval:
      self.last_run = now
      return self.func(*args,**kwargs)

# function for filtering data from controller
def CoolDown(interval):
  def applyDecorator(func):
    decorator = CoolDownDecorator(func=func,interval=interval)
    return wraps(func)(decorator)
  return applyDecorator

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.thread_manager = QThreadPool()
        
        self.stop_flag = False

        self.signalDataArray = signalDataArray([])
        
        self.serial_ports_combo = QComboBox(self)
        self.serial_ports = serial.tools.list_ports.comports()
        serial_ports_desc = [port.name for port in self.serial_ports]
        self.serial_ports_combo.addItems(serial_ports_desc)
        self.serial_ports_combo_label = QLabel('Выберите порт', self)
        self.serial_ports_combo_label.setBuddy(self.serial_ports_combo)        

        self.fs_params_label = QLabel('Текущий сигнал', self)
        self.fs_toggle_button = QPushButton('ВКЛ/ВЫКЛ', self)
        self.fs_toggle_button.setCheckable(True)
        self.fs_toggle_button.clicked.connect(self.set_signal)
        self.fs_params_label.setBuddy(self.fs_toggle_button)
        
        active_label_layout = QHBoxLayout()
        active_label_layout.setDirection(QHBoxLayout.RightToLeft)
        self.active_label = QLabel('Выберите сигнал', self)
        active_label_layout.addWidget(self.active_label)

        self.fs_signal_form_combo = QComboBox(self)
        self.fs_signal_form_combo.addItems(signal_types)
        self.fs_signal_form_combo_label = QLabel('Форма сигнала', self)
        self.fs_signal_form_combo_label.setBuddy(self.fs_signal_form_combo)

        """
        self.fs_signal_duration_type_combo = QComboBox(self)
        self.fs_signal_duration_type_combo.addItems(["Непрерывный", "Одиночный"])
        self.fs_signal_duration_type_label = QLabel("Тип продолжительности сигнала", self)
        self.fs_signal_duration_type_label.setBuddy(self.fs_signal_duration_type_combo)
        """

        self.signal_plot = SignalPlotWidget()
        self.spectre_plot = SpectrePlotWidget()

        self.fs_frequency_spin = QSpinBox()
        self.fs_frequency_spin.setRange(0, 200_000)
        self.fs_frequency_spin.setValue(1)
        self.fs_frequency_label = QLabel('Частота, Гц')
        self.fs_frequency_label.setBuddy(self.fs_frequency_spin)

        self.fs_amplitude_spin = QSpinBox()
        self.fs_amplitude_spin.setRange(0, 200_000)
        self.fs_amplitude_spin.setValue(1)
        self.fs_amplitude_label = QLabel('Амплитуда, В')
        self.fs_amplitude_label.setBuddy(self.fs_amplitude_spin)

        serial_ports_layout = QHBoxLayout()
        serial_ports_layout.addWidget(self.serial_ports_combo_label)
        serial_ports_layout.addWidget(self.serial_ports_combo)

        fs_params_layout = QVBoxLayout()

        fs_switch_layout = QHBoxLayout()
        fs_switch_layout.addWidget(self.fs_params_label)
        fs_switch_layout.addWidget(self.fs_toggle_button)

        fs_signal_form_layout = QHBoxLayout()
        fs_signal_form_layout.addWidget(self.fs_signal_form_combo_label)
        fs_signal_form_layout.addWidget(self.fs_signal_form_combo)

        """
        fs_signal_duration_type_layout = QHBoxLayout()
        fs_signal_duration_type_layout.addWidget(self.fs_signal_duration_type_label)
        fs_signal_duration_type_layout.addWidget(self.fs_signal_duration_type_combo)
        """

        fs_frequency_input_layout = QHBoxLayout()
        fs_frequency_input_layout.addWidget(self.fs_frequency_label)
        fs_frequency_input_layout.addWidget(self.fs_frequency_spin)

        fs_amplitude_input_layout = QHBoxLayout()
        fs_amplitude_input_layout.addWidget(self.fs_amplitude_label)
        fs_amplitude_input_layout.addWidget(self.fs_amplitude_spin)

        fs_signal_buttons_input_layout = QHBoxLayout()
        self.add_signal_button = QPushButton('Добавить сигнал', self)
        self.edit_signal_button = QPushButton('Изменить текущий сигнал', self)
        fs_signal_buttons_input_layout.addWidget(self.add_signal_button)
        fs_signal_buttons_input_layout.addWidget(self.edit_signal_button)
        
        fs_params_layout.addLayout(fs_switch_layout)
        fs_params_layout.addLayout(active_label_layout)
        fs_params_layout.addLayout(fs_signal_form_layout)
        #fs_params_layout.addLayout(fs_signal_duration_type_layout)
        fs_params_layout.addLayout(fs_frequency_input_layout)
        fs_params_layout.addLayout(fs_amplitude_input_layout)
        fs_params_layout.addLayout(fs_signal_buttons_input_layout)
     
        self.signals_label = QLabel('Список сигналов')
        self.signals_list = QComboBox(self)
        self.signals_label.setBuddy(self.signals_list)

        signals_list_layout = QHBoxLayout()
        signals_list_layout.addWidget(self.signals_label)
        signals_list_layout.addWidget(self.signals_list)
        
        ampl_layout = QVBoxLayout()
        self.ampl_create_button = QPushButton('Амплитудная модуляция')
        self.ampl_create_button.clicked.connect(self.click_amplitude_event)
        self.freq_create_button = QPushButton('Частотная модуляция')
        self.freq_create_button.clicked.connect(self.click_frequency_event)
        self.sum_create_button = QPushButton('Множественное суммирование сигналов')
        self.sum_create_button.clicked.connect(self.click_sum_event)
        self.real_signal_button = QPushButton('Работа с реальными сигналами')
        self.real_signal_button.clicked.connect(self.click_real_signal_event)

        self.anim_checkbox = QCheckBox("Включить анимацию")     
        self.real_data_get_mod = QCheckBox("Включить отрисовку в режиме реального времени")   
        self.data_mod_label = QLabel("Режим работы микроконтроллера")
        self.data_mod = QComboBox()
        self.data_mod.addItems(['Получение напряжения в цепи', 'Генерация синуса']) 
        self.data_mod_label.setBuddy(self.data_mod)

        checkbox_params_layout = QVBoxLayout()
        checkbox_params_layout.addWidget(self.anim_checkbox)
        checkbox_params_layout.addWidget(self.real_data_get_mod)

        mc_mode_layout = QVBoxLayout()
        mc_mode_layout.addWidget(self.data_mod_label)
        mc_mode_layout.addWidget(self.data_mod)

        all_params_layout = QHBoxLayout()
        all_params_layout.addLayout(checkbox_params_layout)
        all_params_layout.addLayout(mc_mode_layout)

        ampl_layout.addLayout(signals_list_layout)
        ampl_layout.addWidget(self.ampl_create_button)
        ampl_layout.addWidget(self.freq_create_button)
        ampl_layout.addWidget(self.sum_create_button)
        ampl_layout.addWidget(self.real_signal_button)
        ampl_layout.addLayout(all_params_layout)

        params_layout = QHBoxLayout()
        params_layout.addLayout(fs_params_layout)
        params_layout.addLayout(ampl_layout)
        plot_params_layout = QVBoxLayout()
        plot_params_scale_y = QVBoxLayout()
        self.scale_y_label = QLabel("Маштаб графика")

        plot_params_scale_y.addWidget(self.scale_y_label)

        mechanical_slider_amplitude_layout = QVBoxLayout()
        self.amplitude_lable = QLabel("Ось y")
        self.mechanical_slider_amplitude = QDial()
        self.mechanical_slider_amplitude.setRange(0, 12)
        self.mechanical_slider_amplitude.setValue(6)
        mechanical_slider_amplitude_layout.addWidget(self.amplitude_lable)
        mechanical_slider_amplitude_layout.addWidget(self.mechanical_slider_amplitude)
        self.mechanical_slider_amplitude.valueChanged.connect(self.slider_frequency_move)
               
        mechanical_slider_frequency_layout = QVBoxLayout()
        self.frequency_lable = QLabel("Ось x")
        self.mechanical_slider_frequency = QDial()
        self.mechanical_slider_frequency.setRange(0, 12)
        self.mechanical_slider_frequency.setValue(6)
        mechanical_slider_frequency_layout.addWidget(self.frequency_lable)
        mechanical_slider_frequency_layout.addWidget(self.mechanical_slider_frequency)
        self.mechanical_slider_frequency.valueChanged.connect(self.slider_frequency_move)

        plot_params_layout.addLayout(plot_params_scale_y)
        plot_params_layout.addLayout(mechanical_slider_amplitude_layout)
        plot_params_layout.addLayout(mechanical_slider_frequency_layout)
        plot_params_layout.addStretch()

        plots_layout = QHBoxLayout()
        plots_layout.addLayout(plot_params_layout)
        plots_layout.addWidget(self.signal_plot)
        plots_layout.addWidget(self.spectre_plot)        

        self.com_error_message = QErrorMessage()
        self.receive_button = QPushButton('Начать получение сигнала от МК')
        self.stop_listening_button = QPushButton('Завершить получение сигнала от МК')
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(serial_ports_layout)
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
        self.anim_checkbox.toggled.connect(self.changed_animation_checkbox_event)
        self.real_data_get_mod.toggled.connect(self.real_data_get_mod_changed)
        #self.data_mod.currentIndexChanged.connect()
        self.x_scale_value = 1.1
        self.y_scale_value = 1.1
        self.animation_flag = 0

        self.amplitude_window = AmplitudeWindow(self.signalDataArray)
        self.frequency_window = FrequencyWindow(self.signalDataArray)
        self.summation_window = SummationWindow(self.signalDataArray)
        self.real_signal_window = RealSignalWindow()   
        self.showMaximized()

        self.first_contact = 1
        self.buf1 = dict()
        self.buf2 = dict()
        self.is_online = False
        self.f = open("Data.txt", "w+")

        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

    def real_data_get_mod_changed(self):
        self.is_online = not self.is_online

    def addSignal(self):
        if self.fs_signal_form_combo.currentText() == "-":
            return 

        form_name = self.fs_signal_form_combo.currentText()
        amplitude = self.fs_amplitude_spin.value()
        frequency = self.fs_frequency_spin.value()
        duration_type = 0#self.fs_signal_duration_type_combo.currentIndex()
        self.signalDataArray.appendSignal(signalData(form_name, amplitude, frequency, self.x_scale_value, False, duration_type))
        self.loadSignals()
    
    def loadSignals(self):  
        self.signals_list.clear()      
        data = self.signalDataArray.getArray()
        if len(data) == 0:
            self.signals_list.addItem("Новый сигнал")
        else:
            for i in range(len(data)):
                self.signals_list.addItem('Сигнал ' + str(i + 1))
            self.signals_list.addItem('Новый сигнал')

    def editSignal(self):
        form_name = self.fs_signal_form_combo.currentText()
        amplitude = self.fs_amplitude_spin.value()
        frequency = self.fs_frequency_spin.value()
        duration_type = 0#self.fs_signal_duration_type_combo.currentIndex()
        curInd = self.signals_list.currentIndex()
        if ((curInd != self.signalDataArray.getArraySize()) 
        and (curInd != -1)):
            self.signalDataArray.editSignalByIndex(signalData(form_name, amplitude, frequency, self.x_scale_value, False, duration_type), curInd)
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
            self.fs_frequency_spin.setValue(1)
        elif self.signals_list.currentIndex() != -1:           
            curSignal = self.signalDataArray.getSignalByIndex(self.signals_list.currentIndex()).getData()
            self.fs_signal_form_combo.setCurrentIndex(signal_types.index(curSignal[0]))
            self.fs_amplitude_spin.setValue(curSignal[1])
            self.fs_frequency_spin.setValue(curSignal[2])
            
            if curSignal[4] == True:
                self.active_label.setText("Сигнал активен") 
            else:
                self.active_label.setText("Сигнал неактивен")
            #self.fs_signal_duration_type_combo.setCurrentIndex(curSignal[5])
    
    def set_stop(self):
        self.stop_flag = True

    def set_stop_safely(self):
        self.thread_manager.start(self.set_stop)
        self.setEnable(True) 
        self.stop_flag = True
        if not self.is_online:
            if (len(self.buf2) == 0):
                return
            x, y = generate_data_spectrum(list(self.buf2.values()), max(self.buf2.keys()))       
        else:
            if (len(self.buf1) == 0):
                return
            x, y = generate_data_spectrum(list(self.buf1.values())[-5000:], max(self.buf1.keys()))
        self.spectre_plot.axes.plot(x, y * 2, color='#1f77b4')
        self.spectre_plot.axes.set_ylim(0, max(y * 2) * 1.5)
        self.spectre_plot.axes.set_xlim(0, max(x))
        self.spectre_plot.view.draw()
        self.buf1.clear()
        self.buf2.clear()
        # self.f.close()
       

    #@CoolDown(0.05)
    # function for drawing data from controller
    def reDraw(self, drdata = [], drind = [], left_border = 0):
        try:         
            # if not self.is_online:
            #     self.signal_plot.axes.set_xlim(0, max(drind))
            # else:
            # self.signal_plot.axes.clear()
            self.signal_plot.axes.grid(True)
            #self.y_scale_value = float(self.mechanical_slider_amplitude.value())* 1.1
            self.signal_plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)                  
            self.signal_plot.axes.set_xlabel('Time, s')
            self.signal_plot.axes.set_ylabel('U, V')
            self.signal_plot.axes.plot(drind, drdata, color='#1f77b4')
            self.signal_plot.axes.set_xlim(left_border, max(drind))
            self.signal_plot.view.draw()
        except Exception as e:
                print('error in draw', str(e))

    def receive_signal(self):
        if self.serial_ports_combo.currentText() == '-':
            self.stop_flag = True
            return         
        else:
            self.stop_flag = False
            generator_name = self.serial_ports_combo.currentText()
            try:
                for port in self.serial_ports:
                    if generator_name == port.name:
                        print("Found serial port")
                        if 'serial' in port.description.lower() or 'VCP' in port.description.lower():
                            # init serial port and bound
                            # bound rate on two ports must be the same
                            #was 9600 // 115200
                            # new params: generator_ser = serial.Serial(generator_name, 76800, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)
                            # generator_ser = serial.Serial(generator_name, baudrate = 115200, timeout=1 )
                            # bound rate was 76800
                            generator_ser = serial.Serial(generator_name, 76800, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS ) 
                            # generator_ser = serial.Serial(generator_name, 9600, stopbits=serial.STOPBITS_TWO, parity=serial.PARITY_EVEN, bytesize=serial.SEVENBITS )
                            generator_ser.flushInput()
                            generator_ser.flushOutput()
                            generator_ser.set_buffer_size(rx_size = 12800, tx_size = 12800)
                            cur_time = 0

                            if self.first_contact:
                                self.first_contact = 0

                                # send to mc work mode (voltage or sinus)
                                print("Bef mode")
                                cur_ind = self.data_mod.currentIndex()
                                if (cur_ind == 0):
                                    generator_ser.write(b"M0")
                                elif (cur_ind == 1):    
                                    generator_ser.write(b"M1")

                                # open connection protocol
                                # 1) PC --> MC (R0)
                                # 2) MC --> PC (A0)
                                # 3) connection established
                                while 1:
                                    try:
                                        # new protocol: generator_ser.write(b"R") # Request
                                        #print("Bef write")
                                        generator_ser.write(b"R0")
                                        # generator_ser.write(bytearray(255))
                                        print("Bef read")
                                        ser_bytes = generator_ser.read(2)
                                        print("In open protocol", ser_bytes)
                                        if (len(ser_bytes)):
                                            if ser_bytes[0] == ord("A") and ser_bytes[1] == ord("0"):
                                            # new protocol: if ser_bytes[0] == ord('A'): # Accept
                                                break
                                    except Exception as exc:
                                        print('error in open connection protocol', str(exc))   

                            last_num = 0
                            start_time = time.perf_counter()

                    
                            while not self.stop_flag: #or (self.stop_flag and generator_ser.inWaiting() != 0): # чтение байтов с порта
                                if (self.stop_flag):
                                    # Close connection
                                    # Me --> C0
                                    # Me <-- C0
                                    # generator_ser.send_break(0)
                                    while (1):
                                        try:
                                            generator_ser.write(b"C0")
                                            ser_bytes = generator_ser.read(2)
                                            print("In close protocol", ser_bytes)
                                            if (len(ser_bytes)):
                                                if ser_bytes[0] == ord("C") and ser_bytes[1] == ord("0"):
                                                    break
                                        except Exception as exc:
                                            print('error in connection close protocol', str(exc)) 
                                    generator_ser.send_break(0)
                                    self.first_contact = 1
                                    # Needed?
                                    break   
                                point_time = time.perf_counter()   
                                ser_bytes = generator_ser.read(2)
                                if len(ser_bytes) != 0:
                                    try:
                                        cur_byte = int.from_bytes(ser_bytes[::-1], "little", signed=False) /1023.0*5.0
                                        if (abs(last_num - cur_byte) > 100):
                                            print(bin(last_num | 0b1000000000000))
                                            print(bin(cur_byte | 0b1000000000000))
                                            print('===========')
                                        last_num = cur_byte
                                        cur_time = float(point_time - start_time)
                                        self.buf1[cur_time] = cur_byte
                                        QApplication.processEvents()
                                        if self.is_online:
                                            # TODO num of points depends on x scale
                                            # now: 1.6 s => 5000 points
                                            # 0.1 (4) s => 312 points
                                            # 0.5 (5) s => 1562 points
                                            # 1 (6) s => 3125 points
                                            # 5 (7) s => 15625 points
                                            # 10 (8) s => 31250 points                                          
                                            if self.mechanical_slider_frequency.value() % 2 == 0:
                                                val = 0.0011 * 10**(self.mechanical_slider_frequency.value() // 2)
                                            else:
                                                val = 0.0055 * 10**(self.mechanical_slider_frequency.value() // 2)
                                            # if (val < 4):
                                            #     ind = 312
                                            # elif (val > 8):
                                            #     ind = 31250
                                            # else:
                                            #     if (val % 2):
                                            #         ind = 1562 * int(pow(10, (val - 5) // 2))
                                            #     else:
                                            #         ind = 312 * int(pow(10, (val - 4) // 2))
                                            print(val)
                                            # ind = 1000
                                            # if len(self.buf1) % 100:
                                            #     self.reDraw(list(self.buf1.values())[-ind:], list(self.buf1.keys())[-ind:])
                                            # if (len(self.buf1) > 31250):
                                            #      self.buf1.pop(min(self.buf1.keys()))

                                            if cur_time / val > 1:
                                                self.reDraw(list(self.buf1.values()), list(self.buf1.keys()), cur_time - val)
                                                
                                            else:
                                                self.reDraw(list(self.buf1.values()), list(self.buf1.keys()))
                                        else:
                                            # if (len(self.buf1) >= 5000):
                                            self.reDraw(list(self.buf1.values()), list(self.buf1.keys()))
                                            self.buf2 = self.buf1
                                            self.buf1.clear()

                                    except Exception as e:
                                        print('error in input', str(e))

                                else:
                                    break

                            print("Stop flag:", self.stop_flag)
                            return
                            
                        else:
                            self.com_error_message.showMessage("К данному порту не подключено серийное устройство")
                            return    
            except Exception as e:
                print('error in common input', str(e))                

    def setEnable(self, val):
        self.fs_signal_form_combo.setEnabled(val)
        self.fs_toggle_button.setEnabled(val)
        self.fs_frequency_spin.setEnabled(val)
        self.fs_amplitude_spin.setEnabled(val)
        self.add_signal_button.setEnabled(val)
        self.edit_signal_button.setEnabled(val)
        self.signals_list.setEnabled(val)
        self.ampl_create_button.setEnabled(val)
        self.freq_create_button.setEnabled(val)
        self.sum_create_button.setEnabled(val)
        self.anim_checkbox.setEnabled(val)

    def receive_signal_safely(self):
        self.stop_flag = False
        self.signal_plot.clear()
        self.spectre_plot.clear()
        self.setEnable(False)      
        self.thread_manager.start(self.receive_signal)
        
    def click_amplitude_event(self):        
        self.amplitude_window.updateSignalData(self.signalDataArray)
        self.amplitude_window.show()
         
    def click_sum_event(self):
        self.summation_window.updateSignalData(self.signalDataArray)
        self.summation_window.show()

    def click_frequency_event(self):        
        self.frequency_window.updateSignalData(self.signalDataArray)
        self.frequency_window.show()

    def click_real_signal_event(self):
        self.real_signal_window.showMaximized()

    def changed_animation_checkbox_event(self):
        if (self.anim_checkbox.isChecked()):
            self.animation_flag = 1
        else:
            self.animation_flag = 0

    def set_signal(self):
        if self.signalDataArray.getArraySize == 0:
            return
        self.signalDataArray.array[self.signals_list.currentIndex()].changeActivity()
        if self.signalDataArray.array[self.signals_list.currentIndex()].getActivity() == True:
            self.active_label.setText("Сигнал активен")
            self.drawSignal()
        else:
            self.active_label.setText("Сигнал неактивен")

            self.signal_plot.clear(self.x_scale_value, self.y_scale_value)
            self.spectre_plot.clear()

    def drawSignal(self):
        ind = self.signals_list.currentIndex()
        sigData = self.signalDataArray.getSignalByIndex(ind).getData()
        self.signal_plot.plot(sigData[0], sigData[2], sigData[1],
        self.x_scale_value, self.y_scale_value, animation_flag=self.animation_flag)#,duration_type= sigData[5])
        self.spectre_plot.plot(sigData[0], sigData[1], sigData[2], sigData[3])#, sigData[5])
    
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
        # if self.stop_flag:
        self.signal_plot.axes.set_xlim(-self.x_scale_value, self.x_scale_value)

        #print("y in freq move", self.y_scale_value)

        self.signal_plot.view.draw()
        self.signal_plot.view.flush_events()

    def closeEvent(self, event):
        if self.amplitude_window.isVisible():
            self.amplitude_window.close()
        if self.frequency_window.isVisible():
            self.frequency_window.close()
        if self.summation_window.isVisible():
            self.summation_window.close()
        if self.real_signal_window.isVisible():
            self.real_signal_window.close()
        print("Main window closed")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
