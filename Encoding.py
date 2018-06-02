from generateSound import *
import numpy as np

#freq_range = [5000, 6000, 7000, 8000]
freq_range = [5000, 5200, 5400, 5600]
zero_freq = [3000]
start_freq = [9000]


def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]  # [2:] to chop off the "0b" part


def generateSignal(bit, freq, numCarrier, duration, bandwidth, zero):
    bitArry = bitfield(bit)
    value = []
    while len(bitArry) != numCarrier:
        bitArry.insert(0, 0)
    print(bitArry)
    for i in range(len(bitArry)):
        if bitArry[i] == 1:
            value.append(freq[i])
    if len(value) == 0:
        return generateSoundCombination(chirp_linear, zero, numCarrier, duration, bandwidth)
    return generateSoundCombination(chirp_linear, value, numCarrier, duration, bandwidth)


def generateFullSignal(bits, startFreq, startDuration, freqRange, zeroFreq, duration, bandwidth):
    nullWave = generateSinFreqDuration(0, 1000, duration)
    waveEncode = nullWave + generateSoundCombination(chirp_linear, startFreq, len(freqRange), startDuration, bandwidth)
    for i in bits:
        waveEncode += nullWave + generateSignal(i, freqRange, len(freqRange), duration, bandwidth, zeroFreq)
    waveEncode += nullWave + generateSoundCombination(chirp_linear, startFreq, len(freqRange), startDuration, bandwidth) + nullWave
    return waveEncode


bitSequence = [13, 11, 12, 3, 8, 10, 1, 9, 4, 5, 14, 7, 0, 6, 15, 2]
waveFinal = generateFullSignal(bitSequence, start_freq, 0.04, freq_range, zero_freq, 0.16, 100)
createWaveFormFile('custom.wav', waveFinal)
