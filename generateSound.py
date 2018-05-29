from __future__ import division
import wave
import struct
from math import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt
import sys

sampleRate = 44100.0  # hertz

def generateSinFreqDuration(magnitude, frequency, duration):
    value = []
    for i in range(int(duration * sampleRate)):
        value.append(int(magnitude * 32767.0 * cos(2 * frequency * pi * float(i) / float(sampleRate))))
    return value


def generateCustom(func, frequency, duration):
    value = []
    for i in range(int(duration * sampleRate)):
        value.append(int(func(i / sampleRate, frequency, duration) * 32767.0))
    return value

def generateCustomChirp(func, frequency, duration, bandwidth):
    value = []
    for i in range(int(duration * sampleRate)):
        value.append(int(func(i / sampleRate, frequency, duration, bandwidth) * 32767.0))
    return value

def combineWaveForm(listWaveForm,duration):
    num = len(listWaveForm)
    num = 4
    value = []
    if len(listWaveForm) == 0:
        value = generateCustomChirp(chirp_linear,3000,duration,500)
        value = [int(x/4) for x in value]
        return value
    for i in range(len(listWaveForm[0])):
        value.append(sum([x[i] for x in listWaveForm]))
    value = [int(x / num) for x in value]
    return value


def createWaveFormFile(name, waveForm):
    wavef = wave.open(name, 'w')
    wavef.setnchannels(1)  # mono
    wavef.setsampwidth(2)
    wavef.setframerate(44100)

    for i in waveForm:
        data = struct.pack('<h', i)
        wavef.writeframesraw(data)

    wavef.writeframes(''.encode())
    wavef.close()


def plotSignal(name):
    spf = wave.open(name, 'r')
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    # If Stereo
    if spf.getnchannels() == 2:
        print('Just mono files')
        sys.exit(0)

    plt.figure(1)
    plt.title('Signal Wave...')
    plt.plot(signal)
    plt.show()


def chirp_linear(time, frequency, duration, bandwidth):
    k = float(bandwidth / duration)
    return sin(2 * pi * (frequency * time + k * 0.5 * time * time))


def chirp_exponential(time, frequency, duration, bandwidth):
    k = ((frequency + bandwidth) / (frequency)) ** (1.0 / duration)
    return sin(2 * pi * frequency * ((k ** ((time % duration) - duration) - 1.0) / (np.log(k))))

def generateSoundCombination(func,freq,duration,bandwidth):
    nullWave = generateSinFreqDuration(0, 1000, duration)
    wave = []
    for i in range(len(freq)):
        if freq[i] == -1:
            wave.append(nullWave)
            continue
        wave.append(generateCustomChirp(func,freq[i],duration,bandwidth))
    return combineWaveForm(wave,duration)



nullWave = generateSinFreqDuration(0, 1000, 0.08)

wave1 = generateCustomChirp(chirp_linear, 6000, 0.08, 500)
wave2 = generateCustomChirp(chirp_linear, 8000, 0.08, 500)
wave3 = generateCustomChirp(chirp_linear, 10000, 0.08, 500)


#waveFinal = nullWave + wave1 + nullWave + wave2 + nullWave + wave3 + nullWave
#freq = [2000,3000,-1,4000,-1,6000,-1, 8000,9000, 10000,11000, 12000]

# plotSignal('custom.wav')
# plt.show()

#freq = np.arange(2000,13000,1000)
# freq = [7000]
# waveFinal = generateSoundCombination(chirp_linear,freq,0.04,500)
# createWaveFormFile('custom.wav', waveFinal)
