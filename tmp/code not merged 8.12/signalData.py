from array import array

class signalData:
    def __init__(self, signalType, amplitude, frequency, duration, isActive = 1):
        self.signalType = signalType
        self.amplitude = amplitude
        self.frequency = frequency
        self.duration = duration
        self.isActive = isActive       

    def getData(self):
        return [self.signalType, self.amplitude, self.frequency, self.duration, self.isActive]

    def changeActivity(self):
        self.isActive = not self.isActive

    def getSignaType(self):
        return self.signalType

    def getAmplitude(self):
        return self.amplitude

    def getFrequency(self):
        return self.frequency

    def getDuration(self):
        return self.duration

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

    def clear(self):
        self.array.clear()

    def getLastSignal(self):
        if len(self.array) != 0:
            return self.array[len(self.array) - 1]
        else:
            return signalData("", 0, 0, 0, 0)

    def removeLast(self):
        self.array.pop()