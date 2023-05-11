import sys
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

        ampl_layout.addLayout(signals_list_layout)
        ampl_layout.addWidget(self.ampl_create_button)
        ampl_layout.addWidget(self.freq_create_button)
        ampl_layout.addWidget(self.sum_create_button)
        ampl_layout.addWidget(self.real_signal_button)
        ampl_layout.addWidget(self.anim_checkbox)

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
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(params_layout)
        main_layout.addLayout(plots_layout)

        self.setLayout(main_layout)
        self.loadSignals()
        self.add_signal_button.clicked.connect(self.addSignal)
        self.signals_list.currentIndexChanged.connect(self.showSignals)
        self.edit_signal_button.clicked.connect(self.editSignal)
        self.anim_checkbox.toggled.connect(self.changed_animation_checkbox_event)
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
""""
    def sin(self):
        x_count = 0.01
        point = 5
        while 1:
            if self.mechanical_slider_frequency.value() % 2 == 0:
                val = 0.0011 * 10**(self.mechanical_slider_frequency.value() // 2)
            else:
                val = 0.0055 * 10**(self.mechanical_slider_frequency.value() // 2)

            x = np.linspace(0, x_count, point)
            frequencies = x * 1
            y = 1 * np.sin(frequencies * (2 * np.pi))
            x_count += 0.01
            point += 5

            if x_count / val > 1:
                if point % 30 == 0:
                    self.signal_plot.axes.plot(x, y, color='#1f77b4')
                    self.signal_plot.axes.set_xlim(x_count - val, max(x))
                    # self.signal_plot.axes.grid(False)
                    self.signal_plot.view.draw()
                    self.signal_plot.view.flush_events()                                 
            else:
                if point % 30 == 0:
                    self.signal_plot.axes.plot(x, y, color='#1f77b4')
                    self.signal_plot.axes.set_xlim(0, max(x))
                    # self.signal_plot.axes.grid(False)
                    self.signal_plot.view.draw()
                    self.signal_plot.view.flush_events()
                    """
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    
    sys.exit(app.exec())
