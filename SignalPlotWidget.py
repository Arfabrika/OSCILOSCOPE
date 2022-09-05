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
    mod_generate_square_wave
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


class SignalPlotWidget(PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.axes.set_xlabel('Time, s')
        self.axes.set_ylabel('U, V')
        self.axes.grid(True)

    def plot(self, signal_name, amplitude, frequency, sample_rate, duration):
        self.clear()
        if signal_name == '-':
            return

        x, y = wave_generators[signal_name](amplitude, frequency, sample_rate, duration)

        self.axes.plot(x, y, color='#1f77b4')

        self.view.draw()

    def polyharmonic(self, fs_signal_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
                     ss_signal_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration):
        self.clear()

        if fs_signal_name == '-' or ss_signal_name == '-':
            return

        fx, fy = wave_generators[fs_signal_name](fs_amplitude, fs_frequency, fs_sample_rate, fs_duration)
        sx, sy = wave_generators[ss_signal_name](ss_amplitude, ss_frequency, ss_sample_rate, ss_duration)

        py = fy + sy

        self.axes.plot(fx, py, color='#1f77b4')
        self.axes.axis('tight')
        self.axes.set_aspect('equal')
        self.axes.autoscale(enable=True)

        self.view.draw()

    def modulate(self, modulation_sensitivity, fs_signal_name, fs_frequency, fs_sample_rate, fs_duration,
                 ss_signal_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration):
        self.clear()

        if fs_signal_name == '-' or ss_signal_name == '-':
            return

        fx, fy = mod_wave_generators[fs_signal_name](fs_frequency, fs_sample_rate, fs_duration)
        sx, sy = mod_wave_generators[ss_signal_name](ss_frequency, ss_sample_rate, ss_duration)

        my = ss_amplitude * (1 + modulation_sensitivity * fy) * sy

        self.axes.plot(my, color='#1f77b4')

        self.view.draw()
