# This Python file uses the following encoding: utf-8
from PlotWidget import PlotWidget

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

        _, y = wave_generators[signal_name](amplitude, frequency, duration)

        self.axes.magnitude_spectrum(y, #Fs=sample_rate, 
        color='#1f77b4')

        self.view.draw()

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

    def modulate(self, fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
        self.clear()

        x, y = specter_modulating(fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude)
        
        self.axes.plot(x, y, color='#1f77b4')
        self.view.draw()

    def freq_modulate(self, fs_frequency, ss_frequency, freq_dev):
        self.clear()
        x, y = freq_modulating_specter(fs_frequency, ss_frequency, freq_dev)
        self.axes.plot(x,y,color='#1f77b4')
        self.view.draw()
