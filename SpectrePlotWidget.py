# This Python file uses the following encoding: utf-8
from PlotWidget import PlotWidget

from wave import (
    generate_sine_wave,
    generate_cosine_wave,
    generate_triangle_wave,
    generate_sawtooth_wave,
    generate_square_wave, specter_modulating,
)

wave_generators = {
    'sine': generate_sine_wave,
    'cosine': generate_cosine_wave,
    'triangle': generate_triangle_wave,
    'sawtooth': generate_sawtooth_wave,
    'square': generate_square_wave,
}


class SpectrePlotWidget(PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.axes.set_xlabel('Frequency, Hz')
        self.axes.set_ylabel('Magnitude')
        self.axes.grid(True)

    def plot(self, signal_name, amplitude, frequency, sample_rate, duration):
        self.clear()

        if signal_name == '-':
            return

        _, y = wave_generators[signal_name](amplitude, frequency, sample_rate, duration)

        self.axes.magnitude_spectrum(y, Fs=sample_rate, color='#1f77b4')

        self.view.draw()

    def polyharmonic(self, fs_signal_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
                     ss_signal_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration):
        self.clear()

        if fs_signal_name == '-' or ss_signal_name == '-':
            return

        fx, fy = wave_generators[fs_signal_name](fs_amplitude, fs_frequency, fs_sample_rate, fs_duration)
        sx, sy = wave_generators[ss_signal_name](ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)

        py = fy + sy

        self.axes.magnitude_spectrum(py, Fs=fs_sample_rate, color='#1f77b4')

        self.view.draw()

    def modulate(self, fs_frequency, fs_sample_rate, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
        self.clear()

        x, y = specter_modulating(fs_frequency, fs_sample_rate, fs_duration, ss_amplitude, ss_frequency, fs_amplitude)

        self.axes.plot(x, y, color='#1f77b4')

        self.view.draw()

        # if fs_signal_name == '-' or ss_signal_name == '-':
        #     return
        #
        # fx, fy = mod_wave_generators[fs_signal_name](fs_frequency, fs_sample_rate, fs_duration)
        # sx, sy = mod_wave_generators[ss_signal_name](ss_frequency, ss_sample_rate, ss_duration)
        #
        # my = ss_amplitude * (1 + modulation_sensitivity * fy) * sy
        #
        # self.axes.magnitude_spectrum(my, Fs=fs_sample_rate, color='#1f77b4')
        #
        # self.view.draw()

