from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator


def readWaveFile(waveFileName):
    fs_rate, signal = wavfile.read(waveFileName)
    l_audio = len(signal.shape)
    if l_audio == 2:
        signal = signal.sum(axis=1) / 2
    N = signal.shape[0]
    secs = N / float(fs_rate)
    Ts = 1.0 / fs_rate  # sampling interval in time

    # print("Frequency sampling", fs_rate)
    # print("Channels", l_audio)
    # print("Complete Samplings N", N)
    # print("secs", secs)
    # print("Timestep between samples Ts", Ts)

    return fs_rate, signal, l_audio, N, secs, Ts


def doFFT(waveFileName, timeUnit):
    fs_rate, signal, l_audio, N, secs, Ts = readWaveFile(waveFileName)
    t = np.arange(0, secs, Ts)

    sampleSize = int(timeUnit / Ts)
    sampleArrayStart = list(range(0, N, sampleSize))
    sampleArrayEnd = list(range(sampleSize - 1, N, sampleSize))
    if len(sampleArrayEnd) > len(sampleArrayStart):
        sampleArrayEnd[-1] = []
    elif len(sampleArrayEnd) < len(sampleArrayStart):
        sampleArrayStart[-1] = []

    sampleList = [[x, y] for x, y in zip(sampleArrayStart, sampleArrayEnd)]
    freq_range = scipy.fftpack.fftfreq(sampleSize, Ts)[range(int(sampleSize / 2))]
    Mag = []
    Phase = []
    #print(sampleList)
    for sample in sampleList:
        fft = scipy.fft(signal[sample[0]:sample[1]])
        fft = fft[range(int(sampleSize / 2))]
        Mag.append(abs(fft))
        Phase.append(np.angle(fft))

    return Mag, Phase, freq_range


def findFreqIndex(freq_list, freq_range, bandwidth):
    startIndex = []
    endIndex = []
    begin = False
    count = 0
    for i in range(len(freq_range)):
        if freq_range[i] >= freq_list[count] and not begin:
            startIndex.append(i)
            begin = True
        if freq_range[i] > freq_list[count] + bandwidth and begin:
            endIndex.append(i - 1)
            begin = False
            count += 1
        if count == len(freq_list):
            break
    index = [[x, y] for x, y in zip(startIndex, endIndex)]
    return index


def findSignal(mag, phase, freq, startFreq, bandwidth):
    index = findFreqIndex([startFreq], freq, bandwidth)
    signalPow = []
    for band in mag:
        signalPow.append(sum(band[index[0][0]:index[0][1]]))

    signalIndex = sorted(range(len(signalPow)), key=lambda i: signalPow[i])[-15:]
    signalIndex.reverse()

    i = range(0, len(signalPow), 1)
    plt.plot(i, signalPow)
    #ml = MultipleLocator(1)
    #Ml = MultipleLocator(10)
    #plt.axes().xaxis.set_minor_locator(ml)
    #plt.axes().xaxis.set_major_locator(Ml)
    plt.grid(True, 'both')
    plt.show()



    while abs(signalIndex[0] - signalIndex[1]) < 50:
        #print(signalIndex[0],signalIndex[1])
        del(signalIndex[1])

    signalIndex = [signalIndex[0], signalIndex[1]]
    signalIndex.sort()
    #print(signalIndex)

    signalIndex[0] += 3
    signalIndex[1] -= 0
    print(signalIndex[0],signalIndex[1])
    return mag[signalIndex[0]:signalIndex[1]], phase[signalIndex[0]:signalIndex[1]], freq


def doIntegral(mag, phase, freq, freq_list, packageSize, bandwidth,freq_target):
    allMsg = []
    signalList = []
    for i in range(int(len(mag) / packageSize)):
        temp = mag[packageSize * i]
        for j in range(1, packageSize):
            temp = [x + y for x, y in zip(temp, mag[packageSize * i + j])]

        signalList.append(temp)
    index = findFreqIndex(freq_list, freq, bandwidth)

    codeIndex = []
    for i in freq_target:
        codeIndex.append(freq_list.index(i))
    totalSignalPow = []


    for i in range(len(signalList)):
        msg = []
        signalPow = []
        for j in range(len(freq_list)):
            signalPow.append(sum(signalList[i][index[j][0]:index[j][1]]))

        maxPower = max(signalPow)
        threshold = maxPower/3
        if signalPow.index(maxPower) == codeIndex[0]:
            msg = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        else:
            for i in range(1,len(codeIndex)):
                if signalPow[codeIndex[i]] > threshold:
                    msg.append(1)
                else:
                    msg.append(0)

        allMsg.append(msg)
        num = 0
        for bit in msg:
            num = (num << 1) | bit
        print(msg, num)
        # plt.plot(freq_list, signalPow)
        # plt.show()
        totalSignalPow.append(signalPow)
    #print(len(signalList))
    #print(index)
    #print(allMsg)
    return allMsg

#
# mag, phase, freq = doFFT('custom.wav', 0.04)
# mag, phase, freq = findSignal(mag, phase, freq, 10000, 250)
# freq_target = list(range(3000,10000,500))
# #print(freq_target)
# freq_list = list(range(2500, 11000, 250))
# doIntegral(mag, phase, freq, freq_list, 8, 250, freq_target)
