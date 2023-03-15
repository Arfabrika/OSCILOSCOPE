# This Python file uses the following encoding: utf-8
import numpy as np
from PlotWidget import PlotWidget
from SignalPlotWidget import SignalPlotWidget

from wave import (
    generate_sine_wave,
    generate_cosine_wave,
    generate_triangle_wave,
    generate_sawtooth_wave,
    generate_square_wave,
    mod_generate_sine_wave,
    mod_generate_cosine_wave,
    mod_generate_triangle_wave,
    mod_generate_sawtooth_wave,
    mod_generate_square_wave,
    specter_modulating,
    freq_modulating_specter
)

wave_generators = {
    'sine': generate_sine_wave,
    'cosine': generate_cosine_wave,
    'triangle': generate_triangle_wave,
    'sawtooth': generate_sawtooth_wave,
    'square': generate_square_wave,
}

mod_wave_generators = {
    'sine': mod_generate_sine_wave,
    'cosine': mod_generate_cosine_wave,
    'triangle': mod_generate_triangle_wave,
    'sawtooth': mod_generate_sawtooth_wave,
    'square': mod_generate_square_wave,
}


class SpectrePlotWidget(PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.event_loop = self
        self.axes.set_xlabel('Frequency, Hz')
        self.axes.set_ylabel('Magnitude')
        self.axes.grid(True)

    def plot(self, signal_name, amplitude, frequency, duration):
        self.clear()

        if signal_name == '-':
            return

        _, y = mod_wave_generators[signal_name](frequency, duration,amplitude)
        self.axes.plot(_, y, color='#1f77b4')
        self.axes.set_title(self.generate_formula_spectr(fs_form_name= signal_name, fs_amplitude= amplitude,fs_frequency= frequency))
        self.axes.set_ylim(0, max(max(y), amplitude) * 2)
        self.view.draw()

    def generate_formula_spectr(self, fs_form_name = "sine", row_formula = "", fs_amplitude=1, fs_frequency=1):
        form = 'Formula: '
        T = str(round(1.0 / fs_frequency, 3))
        if row_formula == "":
            f = SignalPlotWidget.generate_formula(self, fs_form_name, fs_amplitude, fs_frequency)
        else:
            f = row_formula    
        f = f[9::]
        f = f.replace('$', ' ')
        
        form += r'$\frac{1}{' + T + r'}\int_0^{' + T + r'}' + f + r'e^{-i\frac{2\pi kt}{' + T + r'}}\mathrm{d}t$'
        return form

    def polyharmonic(self, fs_signal_name, fs_amplitude, fs_frequency, fs_duration,
                     ss_signal_name, ss_amplitude, ss_frequency, ss_duration):
        self.clear()

        if fs_signal_name == '-' or ss_signal_name == '-':
            return

        fx, fy = wave_generators[fs_signal_name](fs_amplitude, fs_frequency, fs_duration)
        sx, sy = wave_generators[ss_signal_name](ss_amplitude, ss_frequency, ss_duration)

        py = fy + sy

        self.axes.magnitude_spectrum(py, color='#1f77b4')

        self.view.draw()

    def modulate(self, fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude, signalMainArray, signalModuArray):
        self.clear()

        x, y = specter_modulating(fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude)

        self.axes.set_title(self.generate_formula_am(signalMainArray, signalModuArray))
        self.axes.plot(x, y, color='#1f77b4')
        self.view.draw()

    def freq_modulate(self, fs_frequency, ss_frequency, freq_dev):
        self.clear()
        x, y = freq_modulating_specter(fs_frequency, ss_frequency, freq_dev)
        self.axes.plot(x,y,color='#1f77b4')
        self.view.draw()
    
    def generate_formula_am(self, signalMainArray, signalModuArray):
        return 'Formula:' + str(signalMainArray[1]) + ' * cos(' + str(round((2 * np.pi) / (1 / signalMainArray[2]), 2)) + 't) + ' + str(round(((2 * np.pi) / (1 / signalMainArray[2])) * ((signalModuArray[1] / signalMainArray[1]) / 2), 2)) + ' * cos(' + str(round(((2 * np.pi) / (1 / signalMainArray[2])) + ((2 * np.pi) / (1 / signalModuArray[2])), 2)) + ' * t))  + ' + str(round(((2 * np.pi) / (1 / signalMainArray[2])) * ((signalModuArray[1] / signalMainArray[1]) / 2), 2)) + ' * cos(' + str(round(((2 * np.pi) / (1 / signalMainArray[2])) - ((2 * np.pi) / (1 / signalModuArray[2])), 2)) + ' * t))'
