class signalData:
    def __init__(self, signalType, amplitude, frequency, sample_rate, duration):
        self.signalType = signalType
        self.amplitude = amplitude
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.duration = duration

    def getData(self):
        return [self.signalType, self.amplitude, self.frequency, self.sample_rate, self.duration]


class signalDataArray:
    def __init__(self, array):
        self.array = array

    def appendSignal(self, signal):
        self.array.append(signal)

    def getSignalByIndex(self, index):
        return self.array[index]

    def getArraySize(self):
        return len(self.array)

    def getArray(self):
        return self.array