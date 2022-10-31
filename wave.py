import numpy as np
from scipy import signal


def generate_sine_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * np.sin(frequencies * (2 * np.pi))
    return x, y


def generate_cosine_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * np.cos(frequencies * (2 * np.pi))
    return x, y


def generate_triangle_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.sawtooth(frequencies * (2 * np.pi), 0.5)
    return x, y


def generate_sawtooth_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.sawtooth(frequencies * (2 * np.pi), 1)
    return x, y


def generate_square_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.square(frequencies * (2 * np.pi))
    return x, y


def mod_generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = np.sin(frequencies * (2 * np.pi))
    return x, y


def mod_generate_cosine_wave(freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = np.cos(frequencies * (2 * np.pi))
    return x, y


def mod_generate_triangle_wave(freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = signal.sawtooth(frequencies * (2 * np.pi), 0.5)
    return x, y


def mod_generate_sawtooth_wave(freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = signal.sawtooth(frequencies * (2 * np.pi), 1)
    return x, y


def mod_generate_square_wave(freq, sample_rate, duration):
    x = np.linspace(-duration, duration, sample_rate * int(10 / duration) if 10 / duration > 1 else int(sample_rate * duration), endpoint=False)
    frequencies = x * freq
    y = signal.square(frequencies * (2 * np.pi))
    return x, y


def modulating (fs_frequency, fs_sample_rate, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
    x = np.linspace(0, fs_duration, fs_sample_rate * fs_duration, endpoint=False)
    y = []

    t1 = (2 * np.pi) / (1 / ss_frequency)
    t2 = (2 * np.pi) / (1 / fs_frequency)

    for point in x:
        y.append((fs_amplitude + ss_amplitude * np.cos(t1 * point)) * np.cos(t2 * point))

    return x, y

def specter_modulating(fs_frequency, fs_sample_rate, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
    x = np.linspace(0, fs_duration, fs_sample_rate * fs_duration, endpoint=False)
    y = []

    t0 = (2 * np.pi) / (1 / fs_frequency)
    t1 = (2 * np.pi) / (1 / ss_frequency)

    y.append(abs((fs_amplitude * ((ss_amplitude / fs_amplitude) / 2)) * np.cos((t0 - t1) * x.max())))
    y.append(abs(fs_amplitude * np.cos(t0 * x.max())))
    y.append(abs((fs_amplitude * ((ss_amplitude / fs_amplitude) / 2)) * np.cos((t0 + t1) * x.max())))
   
    x = []

    x.append(t0-t1)
    x.append(t0)
    x.append(t0+t1)
    return x, y

def freq_modulating(fs_frequency, fs_sample_rate, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
    x = np.linspace(0, fs_duration - 3, fs_sample_rate * fs_duration * 5, endpoint=False)
    y = []
    
    for point in x:
        #y.append(np.cos(400 * point + 10 * np.sin(25 * point)))
        y.append(fs_amplitude * np.cos(ss_frequency * 2 * np.pi * point + 10 * np.sin(fs_frequency * point * 2 * np.pi)))
    return x, y
