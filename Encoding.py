from generateSound import *
import numpy as np
#range of frequencies used for transmitting data

#freq_range = [5000, 6000, 7000, 8000]
freq_range = [3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500]
zero_freq = [3000]
start_freq = [10000]

#generate spaced 0 and 1's from a given binary sequence
def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]  # [2:] to chop off the "0b" part

#Create waveform based on given binary code sequence
def generateSignal(bit, freq, numCarrier, duration, bandwidth, zero):
    #print(bit)
    bitArry = bitfield(bit)
    value = []
    while len(bitArry) != numCarrier:
        bitArry.insert(0, 0)
    #print(bitArry)
    for i in range(len(bitArry)):
        if bitArry[i] == 1:
            value.append(freq[i])
    if len(value) == 0:
        return generateSoundCombination(chirp_linear, zero, numCarrier, duration, bandwidth)
    return generateSoundCombination(chirp_linear, value, numCarrier, duration, bandwidth)

#
def generateFullSignal(bits, startFreq, startDuration, freqRange, zeroFreq, duration, bandwidth):
    nullWave = generateSinFreqDuration(0, 1000, duration)
    waveEncode = nullWave + generateSoundCombination(chirp_linear, startFreq, len(freqRange), startDuration, bandwidth)
    for i in bits:
        waveEncode += nullWave + generateSignal(i, freqRange, len(freqRange), duration, bandwidth, zeroFreq)
    waveEncode += nullWave + generateSoundCombination(chirp_linear, startFreq, len(freqRange), startDuration, bandwidth) + nullWave
    return waveEncode


# #bitSequence = [13, 11, 12, 3, 8, 10, 1, 9, 4, 5, 14, 7, 0, 6, 15, 2]
#bitSequence = [13,56,178,378,2767,3437,1732,2605]
bitSequence = [8191,3640, 1756, 2478, 3415, 3729, 3653, 1724, 3972, 2557, 2534,
               4045, 531,  38,   1485, 2039, 2286, 1897, 1837, 2041, 3893]
waveFinal = generateFullSignal(bitSequence, start_freq, 0.04, freq_range, zero_freq, 0.16, 250)
createWaveFormFile('custom.wav', waveFinal)
