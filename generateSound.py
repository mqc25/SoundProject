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


def chirp_linear(time, frequency, duration, bandwidth):
    k = float(bandwidth / duration)
    return sin(2 * pi * (frequency * time + k * 0.5 * time * time))


def chirp_exponential(time, frequency, duration, bandwidth):
    k = ((frequency + bandwidth) / (frequency)) ** (1.0 / duration)
    return sin(2 * pi * frequency * ((k ** ((time % duration) - duration) - 1.0) / (np.log(k))))


def generateCustomChirp(func, frequency, duration, bandwidth):
    value = []
    for i in range(int(duration * sampleRate)):
        value.append(int(func(i / sampleRate, frequency, duration, bandwidth) * 32767.0))
    return value


def combineWaveForm(listWaveForm, numCarrier, duration):
    value = []
    for i in range(len(listWaveForm[0])):
        value.append(sum([x[i] for x in listWaveForm]))
    value = [int(x / numCarrier) for x in value]
    return value


def generateSoundCombination(func, freq, numCarrier, duration, bandwidth):
    wave = []
    for i in range(len(freq)):
        wave.append(generateCustomChirp(func, freq[i], duration, bandwidth))
    return combineWaveForm(wave, numCarrier, duration)


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
