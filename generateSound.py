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

def combineWaveForm(listWaveForm):
    num = len(listWaveForm)
    value = listWaveForm[0]
    for i in range(1, num):
        value = [x + y for x, y in zip(value, listWaveForm[i])]

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


nullWave = generateSinFreqDuration(0, 1000, 0.08)

wave1 = generateCustomChirp(chirp_linear, 6000, 0.08, 500)
wave2 = generateCustomChirp(chirp_linear, 8000, 0.08, 500)
wave3 = generateCustomChirp(chirp_linear, 10000, 0.08, 500)


waveFinal = nullWave + wave1 + nullWave + wave2 + nullWave + wave3 + nullWave
createWaveFormFile('custom.wav', waveFinal)
# plotSignal('custom.wav')
# plt.show()
