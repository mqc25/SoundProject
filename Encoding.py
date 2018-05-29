from generateSound import *
import numpy as np

freq_range = [3000,5000,7000,9000]

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]] # [2:] to chop off the "0b" part


def generateSignal(bit,freq, duration, bandwidth):
    bitArry = bitfield(bit)
    value = []
    while len(bitArry) != 4:
        bitArry.insert(0,0)
    print(bitArry)
    for i in range(len(bitArry)):
        if bitArry[i] == 1:
            value.append(freq[i])

    return generateSoundCombination(chirp_linear,value,duration,bandwidth)

nullWave = generateSinFreqDuration(0,1000,0.08)


bitSequence = [13,11,12,3,8,10,1,9,4,5,14,7,0,6,15,2]
num = len(bitSequence)

waveEncode = generateSoundCombination(chirp_linear,[6000],0.04,500) + nullWave
for i in bitSequence:
    waveEncode += generateSignal(i,freq_range,0.08,500) + nullWave


# wave0 = generateSoundCombination(chirp_linear,[7000],0.04,500)
# wave1 = generateSignal(13,freq_range,0.08,500)
# wave2 = generateSignal(11,freq_range,0.08,500)
#
#
# waveFinal = nullWave + wave0 + nullWave + wave1 + nullWave + wave2 + nullWave

createWaveFormFile('custom.wav', waveEncode)
