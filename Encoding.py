from generateSound import *
import numpy as np

freq_range = [3000,4000,5000,6000]

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]] # [2:] to chop off the "0b" part


def generateSignal(bit,freq, duration, bandwidth):
    bitArry = bitfield(bit)
    value = []
    for i in range(len(bitArry)):
        if bitArry[i] == 1:
            value.append(freq[i])

    return generateSoundCombination(chirp_linear,freq,duration,bandwidth)

nullWave = generateSinFreqDuration(0,1000,0.08)

wave0 = generateSoundCombination(chirp_linear,[7000],0.04,500)
wave1 = generateSignal(11,freq_range,0.08,500)
wave2 = generateSignal(13,freq_range,0.08,500)

waveFinal = nullWave + wave0 + nullWave + wave1 + nullWave + wave2 + nullWave

createWaveFormFile('custom.wav', waveFinal)
