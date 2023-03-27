import numpy as np
from scipy import signal, fft

def generate_sine_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * np.sin(frequencies * (2 * np.pi))
    return x, y


def generate_cosine_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * np.cos(frequencies * (2 * np.pi))
    return x, y


def generate_triangle_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.sawtooth(frequencies * (2 * np.pi), 0.5)
    return x, y


def generate_sawtooth_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.sawtooth(frequencies * (2 * np.pi), 1)
    return x, y


def generate_square_wave(amplitude, freq, duration):
    x = np.linspace(-duration, duration, 440 * int(10 / duration) if 10 / duration > 1 else int(440 * duration), endpoint=False)
    frequencies = x * freq
    y = amplitude * signal.square(frequencies * (2 * np.pi))
    return x, y

def mod_generate_sine_wave(freq, duration, ampl):
    num_of_points = 440 * max((int(10 / duration) if 10 / duration > 1 else int(duration)), freq) * freq
    x = np.linspace(0, freq * 2, num_of_points, endpoint=False)
    y = [0] * len(x)
    y[int(freq * num_of_points / max(x))] = ampl
    return x, y

def mod_generate_cosine_wave(freq, duration, ampl):
    num_of_points = 440 * max((int(10 / duration) if 10 / duration > 1 else int(duration)), freq) * freq
    x = np.linspace(0, freq * 2, num_of_points, endpoint=False)
    y = [0] * len(x)
    y[int(freq * num_of_points / max(x))] = ampl
    return x, y


def mod_generate_triangle_wave(freq, duration, ampl):
    num_of_points = 440 * max((int(10 / duration) if 10 / duration > 1 else int(duration)), freq)
    omega = freq * 2 * np.pi
    x = np.linspace(0, 10 if freq <= 5 else freq * 2, num_of_points, endpoint=False)
    y = [0] * len(x)
    i = 1
    
    while int(i * num_of_points / max(x)) < len(x):
        ind = int(i * num_of_points / max(x))
        y[ind] = (ampl * x[ind] / 2) * (np.sin(omega * x[ind] / 4)**2) / ((omega * x[ind] / 4)**2)
        i += 1
    return x, y

def tmp(freq, duration, ampl):
    num_of_points = 440 * max((int(10 / duration) if 10 / duration > 1 else int(duration)), freq)
    T = 1 / freq
    omega = freq * 2 * np.pi
    x = np.linspace(0, 10, num_of_points, endpoint=False)
    y = [0] * len(x)
    i = 1
    for i in range(1, len(x) - 1):
        y[i] = (ampl * x[i] / 2) * (np.sin(omega * x[i] / 4)**2) / ((omega * x[i] / 4)**2)
        #ampl * np.sin(omega * x[i] / 2) / (omega * x[i] / 2)
        if i % 396 == 0:
            print(i, " ", y[i])
        i += 1
    return x, y

def mod_generate_sawtooth_wave(freq, duration):
    num_of_points = 440 * max((int(10 / duration) if 10 / duration > 1 else int(duration)), freq)
    omega = freq * 2 * np.pi
    x = np.linspace(0, 10 if freq <= 5 else freq * 2, num_of_points, endpoint=False)
    y = [0] * len(x)
    i = 0.5
    while int(i * num_of_points / max(x)) < len(x):
        ind = int(i * num_of_points / max(x))
        y[ind] = ampl * np.sin(omega * x[ind] / 2) / (omega * x[ind] / 2)
        i += 0.5
    return x, y
    return x, y


def mod_generate_square_wave(freq, duration, ampl):
    num_of_points = 440 * max((int(10 / duration) if 10 / duration > 1 else int(duration)), freq)
    omega = freq * 2 * np.pi
    x = np.linspace(0, 10 if freq <= 5 else freq * 2, num_of_points, endpoint=False)
    y = [0] * len(x)
    i = 0.5
    while int(i * num_of_points / max(x)) < len(x):
        ind = int(i * num_of_points / max(x))
        y[ind] = ampl * np.sin(omega * x[ind] / 2) / (omega * x[ind] / 2)
        i += 0.5
    return x, y

def modulating (fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
    x = np.linspace(-fs_duration, fs_duration, 440 * int(10 / fs_duration) if 10 / fs_duration > 1 else int(fs_sample_rate * 440), endpoint=False)
    y = []

    t1 = (2 * np.pi) / (1 / ss_frequency)
    t2 = (2 * np.pi) / (1 / fs_frequency)

    for point in x:
        y.append((fs_amplitude + ss_amplitude * np.cos(t1 * point)) * np.cos(t2 * point))

    return x, y

def specter_modulating(fs_frequency, fs_duration, ss_amplitude, ss_frequency, fs_amplitude):
    x = []#np.linspace(0, fs_duration, 440 * fs_duration, endpoint=False)
    y = []

    t1 = (2 * np.pi) / (1 / ss_frequency)
    t2 = (2 * np.pi) / (1 / fs_frequency)

    x.append(fs_frequency - ss_frequency)
    x.append(fs_frequency)
    x.append(fs_frequency + ss_frequency)

    y.append((fs_amplitude * ((fs_amplitude - ss_amplitude) / fs_amplitude) / 2))
    y.append(fs_amplitude)
    y.append((fs_amplitude * ((fs_amplitude - ss_amplitude) / fs_amplitude) / 2))

    x_res = []
    y_res = []
    index = 0
    point = 0

    while round(point, 2) != x[2] + x[0]:
        if round(point, 2) == x[index]:
            y_res.append(y[index])
            if index < 2:
                index += 1
        else:
            y_res.append(0)
        x_res.append(point)
        point += 0.01


    return x_res, y_res

def freq_modulating(fs_frequency, fs_duration, ss_amplitude, ss_frequency, freq_dev):
    # enough points?
    x = np.linspace(-fs_duration, fs_duration, int(fs_duration * 40 * int((ss_frequency + fs_frequency))), endpoint=False)
    y = []
    
    twopi = 2 * np.pi
    for point in x:
        y.append(ss_amplitude * np.cos(ss_frequency * twopi * point + freq_dev * np.sin(fs_frequency * point * twopi)))
    return x, y

def freq_modulating_specter(fs_frequency, ss_frequency, freq_dev):
    beta = freq_dev / fs_frequency
    left = ss_frequency -  (beta + 1) * fs_frequency
    right = ss_frequency +  (beta + 1) * fs_frequency
    x = np.linspace(left, right, int((right - left) * (ss_frequency + fs_frequency) / 4), endpoint=False)
    y = []
    for point in x:
       y.append(0)
    index = len(x) // 2
    i = 0.5
    n = 1
    y[index] = 1
    ind1 = fs_frequency * n * (ss_frequency + fs_frequency) / 4
    while (int(index - ind1) >= 0 and int(index + ind1) < len(x)):
        y[int(index - ind1)] = i
        y[int(index + ind1)] = i
        i /= 2
        n += 1
        ind1 = fs_frequency * n * (ss_frequency + fs_frequency) / 4
    return x, y

def generate_data_spectrum(data, Fs):
    n = len(data)
    k = np.arange(n) #np.linspace(0, n, n, endpoint=False)
    T = Fs#n/Fs #+ 0.5 *((freq + 3) // 5)
    frq = k/T
    frq = frq[range(n//2)]
    spec = fft.fft(data) / n
    spec = spec[range(n//2)] * 2
    spec[0] = 0
    return frq, np.abs(spec)

def phase_modulate(fs_frequency, fs_duration, ss_amplitude, ss_frequency, freq_dev):
    # enough points?
    x = np.linspace(-fs_duration, fs_duration, int(fs_duration * 40 * int((ss_frequency + fs_frequency))), endpoint=False)
    y = []
    
    twopi = 2 * np.pi
    for point in x:
        y.append(ss_amplitude * np.sin(ss_frequency * twopi * point + freq_dev * np.sin(fs_frequency * point * twopi)))
    return x, y

