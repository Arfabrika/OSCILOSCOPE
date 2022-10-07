class signalData:
    def __init__(self, signalType, amplitude, frequency, sample_rate, duration, isActive = 1):
        self.signalType = signalType
        self.amplitude = amplitude
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.duration = duration
        self.isActive = isActive

    def getData(self):
        return [self.signalType, self.amplitude, self.frequency, self.sample_rate, self.duration, self.isActive]

    def changeActivity(self):
        self.isActive = not self.isActive

    def getActivity(self):
        return self.isActive


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

    def editSignalByIndex(self, signal, index):
        self.array[index] = signal