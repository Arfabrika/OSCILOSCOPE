from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QDial,
    QCheckBox,
    QSpacerItem,
    QApplication
)

from PySide6.QtCore import QThreadPool
from PySide6.QtGui import QAction
from SignalPlotWidget import SignalPlotWidget
from SpectrePlotWidget import SpectrePlotWidget
from wave import (generate_data_spectrum)

import serial.tools.list_ports
import time

# from functools import partial, wraps
# class CoolDownDecorator(object):
#   def __init__(self,func,interval):
#     self.func = func
#     self.interval = interval
#     self.last_run = 0
#   def __get__(self,obj,objtype=None):
#     if obj is None:
#       return self.func
#     return partial(self,obj)
#   def __call__(self,*args,**kwargs):
#     now = time.time()
#     if now - self.last_run > self.interval:
#       self.last_run = now
#       return self.func(*args,**kwargs)

# # function for filtering data from controller
# def CoolDown(interval):
#   def applyDecorator(func):
#     decorator = CoolDownDecorator(func=func,interval=interval)
#     return wraps(func)(decorator)
#   return applyDecorator

class RealSignalWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread_manager = QThreadPool()

        self.serial_ports_combo = QComboBox(self)
        self.serial_ports = serial.tools.list_ports.comports()
        serial_ports_desc = [port.name for port in self.serial_ports]
        self.serial_ports_combo.addItems(serial_ports_desc)
        self.serial_ports_combo_label = QLabel('Выберите порт')
        self.empty_widget = QSpacerItem(25,25)
        serial_ports_layout = QVBoxLayout()
        
        serial_ports_layout.addItem(self.empty_widget)
        serial_ports_layout.addWidget(self.serial_ports_combo_label, stretch=0)
        serial_ports_layout.addWidget(self.serial_ports_combo)
        
        self.is_real_data_mod = QCheckBox("Включить отрисовку в режиме реального времени")
        self.data_mod_label = QLabel("Режим работы микроконтроллера")
        self.data_mod = QComboBox()
        self.data_mod.addItems(['Получение напряжения в цепи', 'Генерация синуса']) 
        self.data_mod_label.setBuddy(self.data_mod)

        data_mod_layout = QVBoxLayout()
        data_mod_layout.addWidget(self.data_mod_label)
        data_mod_layout.addWidget(self.data_mod)

        settings_layout = QVBoxLayout()
        settings_layout.addWidget(self.is_real_data_mod)
        settings_layout.addLayout(data_mod_layout)

        main_params_layout = QHBoxLayout()
        main_params_layout.addLayout(serial_ports_layout)
        main_params_layout.addLayout(settings_layout)

        self.signal_plot = SignalPlotWidget()
        self.spectre_plot = SpectrePlotWidget()
        graphic_layout = QHBoxLayout()
        graphic_layout.addWidget(self.signal_plot)
        graphic_layout.addWidget(self.spectre_plot)

        sliders_layout = QVBoxLayout()
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

        sliders_layout.addLayout(plot_params_scale_y)
        sliders_layout.addLayout(mechanical_slider_amplitude_layout)
        sliders_layout.addLayout(mechanical_slider_frequency_layout)
        sliders_layout.addStretch()

        plot_with_sliders_layout = QHBoxLayout()
        plot_with_sliders_layout.addLayout(sliders_layout)
        plot_with_sliders_layout.addLayout(graphic_layout)

        self.receive_button = QPushButton('Начать получение сигнала от МК')
        self.stop_listening_button = QPushButton('Завершить получение сигнала от МК')
        self.receive_button.clicked.connect(self.receive_signal_safely)
        self.stop_listening_button.clicked.connect(self.set_stop_safely)
        self.is_real_data_mod.toggled.connect(self.is_real_data_mod_changed)
        self.data_mod.currentIndexChanged.connect(self.data_mod_index_changed)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.receive_button)
        buttons_layout.addWidget(self.stop_listening_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(main_params_layout)
        main_layout.addLayout(plot_with_sliders_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.x_scale_value = 1.1
        self.y_scale_value = 1.1
        self.first_contact = 1
        self.buf1 = dict()
        self.buf2 = dict()
        self.is_online = False

        finish = QAction("Quit", self)
        finish.triggered.connect(self.closeEvent)

    def change_singal_mode(self):
        # send to mc work mode
        # 0 - Voltage measuring
        # 1 - Sinus generation
        if (self.generator_ser):
            cur_ind = self.data_mod.currentIndex()
            if (cur_ind == 0):
                self.generator_ser.write(b"M0")
                print("Voltage", self.generator_ser)
            elif (cur_ind == 1):    
                self.generator_ser.write(b"M1")
                print("Sinus", self.generator_ser)
            while 1: 
                ser_bytes = self.generator_ser.read(2)
                print("In mode changing", chr(ser_bytes[0]), chr(ser_bytes[1]))
                if (ser_bytes[0] == ord("A") and ser_bytes[1] == ord("1")):
                    break
            print('end')
            #ser_bytes = self.generator_ser.read(2)
            #print(ser_bytes)

    def is_real_data_mod_changed(self):
        self.is_online = not self.is_online

    def data_mod_index_changed(self):
        print("changed")
        #self.thread_manager.start(self.change_singal_mode)
        self.change_singal_mode()

    def receive_signal_safely(self):
        self.stop_flag = False
        self.signal_plot.clear()
        self.spectre_plot.clear()
        self.setEnable(False)      
        self.thread_manager.start(self.receive_signal)

    #@CoolDown(0.05)
    # function for drawing data from controller
    def reDraw(self, drdata = [], drind = []):
        try:         
            if not self.is_online:
                self.signal_plot.axes.set_xlim(0, max(drind))
            else:
                self.signal_plot.axes.clear()
                self.signal_plot.axes.grid(True)
            #self.y_scale_value = float(self.mechanical_slider_amplitude.value())* 1.1
            self.signal_plot.axes.set_ylim(-self.y_scale_value, self.y_scale_value)                  
            self.signal_plot.axes.set_xlabel('Time, s')
            self.signal_plot.axes.set_ylabel('U, V')
            self.signal_plot.axes.plot(drind, drdata, color='#1f77b4')
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
                            # new params: self.generator_ser = serial.Serial(generator_name, 76800, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS)
                            # self.generator_ser = serial.Serial(generator_name, baudrate = 115200, timeout=1 )
                            # bound rate was 76800
                            self.generator_ser = serial.Serial(generator_name, 76800, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS )
                            self.generator_ser.flushInput()
                            self.generator_ser.flushOutput()
                            self.generator_ser.set_buffer_size(rx_size = 12800, tx_size = 12800)
                            cur_time = 0

                            if self.first_contact:
                                self.first_contact = 0

                                
                                print("Bef mode")
                                self.change_singal_mode()

                                # open connection protocol
                                # 1) PC --> MC (R0)
                                # 2) MC --> PC (A0)
                                # 3) connection established
                                while 1:
                                    try:
                                        #print("Bef write")
                                        self.generator_ser.write(b"R0")
                                        #print("Bef read")
                                        ser_bytes = self.generator_ser.read(2)
                                        print("In open protocol", ser_bytes)
                                        if (len(ser_bytes)):
                                            if ser_bytes[0] == ord("A") and ser_bytes[1] == ord("0"):
                                                break
                                    except Exception as exc:
                                        print('error in open connection protocol', str(exc))   

                            last_num = 0
                            start_time = time.perf_counter()
                            print("bef wh")
                            while not self.stop_flag:
                                if (self.stop_flag):
                                    # Close connection
                                    # Me --> C0
                                    # Me <-- C0
                                    # self.generator_ser.send_break(0)
                                    while (1):
                                        try:
                                            self.generator_ser.write(b"C0")
                                            ser_bytes = self.generator_ser.read(2)
                                            print("In close protocol", ser_bytes)
                                            if (len(ser_bytes)):
                                                if ser_bytes[0] == ord("C") and ser_bytes[1] == ord("0"):
                                                    break
                                        except Exception as exc:
                                            print(exc)
                                            print('error in connection close protocol', str(exc)) 
                                    #self.generator_ser.send_break(0)
                                    self.first_contact = 1
                                    # Needed?
                                    break   
                                print("bef p")
                                point_time = time.perf_counter()   
                                ser_bytes = self.generator_ser.read(2)
                                print("af r", ser_bytes)
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
                                            val = self.mechanical_slider_frequency.value() + 1
                                            """if (val < 4):
                                                ind = 312
                                            elif (val > 8):
                                                ind = 31250
                                            else:
                                                if (val % 2):
                                                    ind = 1562 * int(pow(10, (val - 5) // 2))
                                                else:
                                                    ind = 312 * int(pow(10, (val - 4) // 2))
                                            # 
                                            # ind = 1000"""
                                            """
                                            if (val % 2):
                                                    ind = 50 * int(pow(10, (val) // 2))
                                                else:
                                                    ind = 10 * int(pow(10, (val) // 2))
                                            """
                                            #ind = int(len(self.buf1) / 12) * val
                                            ind = 500
                                            #print(len(self.buf1))
                                            self.reDraw(list(self.buf1.values())[-ind::10], list(self.buf1.keys())[-ind::10])
                                            if (len(self.buf1) % 100 == 0):
                                                print(len(self.buf1))
                                            if (len(self.buf1) > 31250):
                                                 self.buf1.pop(min(self.buf1.keys()))
                                        else:
                                            if (len(self.buf1) >= 100):
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
    
    def setEnable(self, state):
        self.receive_button.setEnabled(state)
        self.serial_ports_combo.setEnabled(state)

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

    def closeEvent(self, event):
        if self.first_contact == False:
            self.set_stop_safely()
        print("Real signal window closed")