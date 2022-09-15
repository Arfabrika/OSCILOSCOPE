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

        self.axes.set_title(self.generate_formula(signal_name, amplitude, frequency, sample_rate, duration))

        self.axes.plot(x, y, color='#1f77b4')

        self.view.draw()

    def generate_formula(self, fs_form_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
                               ss_form_name = '-', ss_amplitude =1, ss_frequency=1, ss_sample_rate=1, ss_duration=1):
        form = 'Formula is: '
        """
        if (ss_form_name != '-' and fs_form_name != '-'):
             form = 'a'
        elif (ss_form_name != '-'):
            form = 'b'
        elif (fs_form_name != '-'):
        """
        if (fs_form_name == 'sine'):
            form += str(fs_amplitude) + 'sin(' + str(fs_frequency) + 't)'
        elif (fs_form_name == 'cosine'):
            form += str(fs_amplitude) +'cos(' + str(fs_frequency) + 't)'
        elif (fs_form_name == 'square'):
            form += r'$\frac{4\cdot'+ str(fs_amplitude) + r'}{\pi}\sum_{k=1}^\infty \frac{sin(k\cdot' + str(fs_frequency) +  r'\cdot t)}{k}$'   
        elif (fs_form_name == 'triangle'):
            form += r'$\frac{8\cdot'+ str(fs_amplitude) + r'}{\pi^{2}}\sum_{k=1}^\infty (-1)^{\frac{k-1}{2}} \cdot \frac{  sin(k\cdot'+ str(fs_frequency) + r'\cdot t)}{k^{2}}$'
        else:
            form += r'$\frac{' + str(fs_amplitude) + r'}{2} - \frac{'+ str(fs_amplitude) + r'}{\pi}\sum_{k=1}^\infty \frac{1}{k} \cdot sin(k\cdot' + str(fs_frequency) +  r'\cdot t)$'   
        return form

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
        self.axes.autoscale(enable=True) # ???
        self.axes.set_title(self.generate_formula(fs_signal_name, fs_amplitude, fs_frequency, fs_sample_rate, fs_duration,
                     ss_signal_name, ss_amplitude, ss_frequency, ss_sample_rate, ss_duration))

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
