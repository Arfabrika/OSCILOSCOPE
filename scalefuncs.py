def getAxisNames(x_scale_type, y_scale_type):
    x_name = 'Time, s'
    y_name = 'U, V'
    if (x_scale_type == 1):
        x_name = 'Time, min'
    elif (x_scale_type == -1):
        x_name = 'Time, ms'
    elif (x_scale_type == -2):
        x_name = 'Time, µs'
    if (y_scale_type == 1):
        y_name = 'U, kV'
    elif (y_scale_type == -1):
        y_name = 'U, mV'
    elif (y_scale_type == -2):
        y_name = 'U, µV'
    return x_name, y_name

def getScaleType(frequency, amplitude):
    x_type = 0
    y_type = 0
    if (frequency <= 0.01):
        x_type = 1
    elif (frequency >= 100 and frequency < 100000):
        x_type = -1
    elif (frequency >= 100000):
        x_type = -2
    if (amplitude <= 0.01):
        y_type = 1
    elif (amplitude >= 100 and frequency < 100000):
        y_type = -1
    elif (amplitude >= 100000):
        y_type = -2
    return x_type, y_type
    

def getScaledParams(frequency, amplitude, x_scale_type = 0, y_scale_type = 0):
    if (x_scale_type == 1):
        frequency *= 60
    elif (x_scale_type == -1):
        frequency /= 1000
    elif (x_scale_type == -2):
        frequency /= 1000000
    if (y_scale_type == 1):
        amplitude *= 1000
    elif (y_scale_type == -1):
        amplitude /= 1000
    elif (y_scale_type == -2):
        amplitude /= 1000000
    return frequency, amplitude

def getScaledParamsInMas(freq_mas, ampl_mas, x_type_mas, y_type_mas):
    if len(freq_mas) == 0 or len(ampl_mas) == 0 or len(x_type_mas) == 0 or len (y_type_mas) == 0:
        print("Empty array in getScaledParamsInMas")
        return [], []
    min_x_type = min(x_type_mas)
    min_y_type = min(y_type_mas)
    for i, value in enumerate(freq_mas):
        freq_mas[i], ampl_mas[i] = getScaledParams(freq_mas[i], ampl_mas[i], min_x_type, min_y_type)
    return freq_mas, ampl_mas