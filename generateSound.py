from __future__ import division
import wave
import struct
import math
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.fftpack import fft
from scipy.io import wavfile # get the api


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
        value.append(int(magnitude*32767.0*math.cos(2*frequency*math.pi*float(i)/float(sampleRate))))
    return value

def generateWaveFormCustom(func,frequency,duration):
    value = []
    for i in range(int(duration * sampleRate)):
        value.append(int(func(i/sampleRate)*32767.0*math.cos(2*frequency*math.pi*float(i)/float(sampleRate))))

    return value

def generateCustom(func,duration):
    value = []
    for i in range(int(duration * sampleRate)):
        value.append(int(func(i/sampleRate)*32767.0))
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

def func3(time):
    return 0.5*math.sin(2*math.pi*3000*time) + 0.5*math.sin(2*math.pi*2000*time)

def func4(time):
    return 0.5*math.sin(2*math.pi*2000*time) + 0.5*math.sin(2*math.pi*1000*time)

def func5(time):
    sum = 0
    for i in range(1, 11):
        sum += 0.1 * math.sin(2 * math.pi * 1000*i * time)
    return sum

def func6(time):
    sum = 0
    for i in range(1, 11):
        sum += 0.1 * math.sin(2 * math.pi * (2000 + 100*i) * time)
    return sum


freq = 5000

# wave1 = generateSinFreqDuration(0,freq,1)
# wave2 = generateWaveFormCustom(func1,freq,1)
# wave3 = generateSinFreqDuration(0,freq,1)
# wave4 = generateWaveFormCustom(func2,freq,1)
# wave5 = generateSinFreqDuration(0,freq,1)
# wave6 = generateSinFreqDuration(1,freq,1)

waveNull = generateSinFreqDuration(0,3000,1)

# wave11 = generateSinFreqDuration(1,1000,1)
# wave12 = generateSinFreqDuration(1,2000,1)
# wave10 = combineWaveForm([wave11,wave12])
#
# wave21 = generateSinFreqDuration(1,2000,1)
# wave22 = generateSinFreqDuration(1,3000,1)
# wave20 = combineWaveForm([wave21,wave22])
#
# wave30 = generateSinFreqDuration(1,2000,1)

wave10 = generateCustom(func5,1)
wave20 = generateCustom(func6,1)

waveFinal = waveNull + wave10 + waveNull + wave20 + waveNull
createWaveFormFile('custom.wav',waveFinal)
#plotSignal('custom.wav')
#plt.show()

#
# plt.figure(1)
# plt.subplot(211)
# plotSignal('sound.wav')
# plt.subplot(212)
# plotSignal('record.wav')
# plt.show()
