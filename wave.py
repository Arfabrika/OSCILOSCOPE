import numpy as np
from scipy import signal


def generate_sine_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = amplitude * np.sin(frequencies * (2 * np.pi))
    return x, y


def generate_cosine_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = amplitude * np.cos(frequencies * (2 * np.pi))
    return x, y


def generate_triangle_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.sawtooth(frequencies * (2 * np.pi), 0.5)
    return x, y


def generate_sawtooth_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.sawtooth(frequencies * (2 * np.pi), 1)
    return x, y


def generate_square_wave(amplitude, freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.square(frequencies * (2 * np.pi))
    return x, y


def mod_generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = np.sin(frequencies * (2 * np.pi))
    return x, y


def mod_generate_cosine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = np.cos(frequencies * (2 * np.pi))
    return x, y


def mod_generate_triangle_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = signal.sawtooth(frequencies * (2 * np.pi), 0.5)
    return x, y


def mod_generate_sawtooth_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = signal.sawtooth(frequencies * (2 * np.pi), 1)
    return x, y


def mod_generate_square_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    y = signal.square(frequencies * (2 * np.pi))
    return x, y