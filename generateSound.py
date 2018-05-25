from __future__ import division
import wave
import struct
import math
import numpy as np
import matplotlib.pyplot as plt
import sys

sampleRate = 44100.0 # hertz
# duration = 1.0       # seconds
# frequency = [1000]    # hertz
#
# wavef = wave.open('sound.wav','w')
# wavef.setnchannels(1) # mono
# wavef.setsampwidth(2)
# wavef.setframerate(sampleRate)


def generateSinFreqDuration(magnitude,frequency, duration):
    value = []
    for i in range(int(duration * sampleRate)):
        value.append(int(magnitude*32767.0*math.cos(frequency*math.pi*float(i)/float(sampleRate))))
    return value

def generateWaveFormCustom(func,frequency,duration):
    value = []
    for i in range(int(duration * sampleRate)):
        value.append(int(func(i/sampleRate)*32767.0*math.cos(frequency*math.pi*float(i)/float(sampleRate))))

    return value


def combineWaveForm(listWaveForm):
    num = len(listWaveForm)
    value = listWaveForm[0]
    for i in range(2,num):
        value = [x+y for x,y in zip(value,listWaveForm[i])]

    value = [int(x/num) for x in value]
    return value

def createWaveFormFile(name,waveForm):
    wavef = wave.open(name, 'w')
    wavef.setnchannels(1)  # mono
    wavef.setsampwidth(2)
    wavef.setframerate(44100)

    for i in waveForm:
        data = struct.pack('<h',i)
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
    #plt.show()

def func1(time):
    return 0.1*math.sin(time) + 0.5*math.cos(time)

def func2(time):
    return 0.5*math.sin(time) + 0.1*math.cos(time)

wave1 = generateSinFreqDuration(0,1000,1)
wave2 = generateWaveFormCustom(func1,1000,1)
wave3 = generateSinFreqDuration(0,1000,1)
wave4 = generateWaveFormCustom(func2,1000,1)
wave5 = generateSinFreqDuration(0,1000,1)

waveFinal = wave1 + wave2 + wave3 + wave4 + wave5
print(wave1)
createWaveFormFile('custom.wav',waveFinal)
plotSignal('custom.wav')
plt.show()
#
# plt.figure(1)
# plt.subplot(211)
# plotSignal('sound.wav')
# plt.subplot(212)
# plotSignal('record.wav')
# plt.show()
