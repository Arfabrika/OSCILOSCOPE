from array import array


class signalData:
    def __init__(self, signalType, amplitude, frequency, sample_rate, duration, isActive = 1, xscale = 0, yscale = 0):
        self.signalType = signalType
        self.amplitude = amplitude
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.duration = duration
        self.isActive = isActive
        self.xscale = xscale
        self.yscale = yscale
        """
        x < 100 => xscale = 0
        10000 >= x >= 100 => xscale = 1
        x >= 100000 => xscale = 2

        -//- with y
        """

    def getData(self):
        return [self.signalType, self.amplitude, self.frequency, self.sample_rate, self.duration, self.isActive, self.xscale, self.yscale]

    def changeActivity(self):
        self.isActive = not self.isActive

    def getSignaType(self):
        return self.signalType

    def getAmplitude(self):
        return self.amplitude

    def getFrequency(self):
        return self.frequency

    def getSampleRate(self):
        return self.sample_rate

    def getDuration(self):
        return self.duration

    def getActivity(self):
        return self.isActive

    def getXScale(self):
        return self.xscale

    def getYScale(self):
        return self.yscale


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

    def clear(self):
        self.array.clear()

    def getLastSignal(self):
        if len(self.array) != 0:
            return self.array[len(self.array) - 1]
        else:
            return signalData("", 0, 0, 0, 0)

    def removeLast(self):
        self.array.pop()
