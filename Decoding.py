import numpy as np
from fft import *
import matplotlib.pyplot as plt

max_threshold = 0

def getStartEndIndex(freq_list, freq_range, bandwidth):
    countStart = 0
    countEnd = 0

    indexStart = []
    indexEnd = []
    for i in range(len(freq_range)):
        if countStart < len(freq_list) and freq_range[i] > freq_list[countStart]:
            indexStart.append(i)
            countStart += 1

        if (freq_range[i] > freq_list[countEnd] + bandwidth):
            indexEnd.append(i)
            countEnd += 1
            if countEnd == len(freq_list):
                return indexStart, indexEnd

def getIntegral(indexStart, indexEnd, FFT):
    value = []
    for i in range(len(indexStart)):
        value.append(sum(FFT[indexStart[i]:indexEnd[i]]))
    return value

def findFirstIndex(waveFileName):
    time_chunk, freq_oneside_chunk, FFT_side_chunk, FFT_phase_chunk = performFFTinChunk(waveFileName, 0.04)
    freq = [9500]
    result_chunk = []

    time_start = []

    start_pos = None
    done = False
    for i in range(len(freq_oneside_chunk)):
        indexStart, indexEnd = getStartEndIndex(freq, freq_oneside_chunk[i], 500)
        resultTemp = getIntegral(indexStart, indexEnd, FFT_side_chunk[i])
        result_chunk.append(resultTemp)
        time_start.append(time_chunk[i][0])

    start_pos = result_chunk.index(max(result_chunk))
    max_threshold = max(result_chunk)
    print(time_start[start_pos], start_pos)
    plt.plot(time_start, result_chunk)
    plt.show()

    return start_pos, time_chunk


def getPackage(waveFileName, start_i, numPackage, time):
    time_start = []
    time_end = []
    for i in range(numPackage):
        time_start.append(time[start_i + 2 + 8 * i][0])
        time_end.append(time[start_i + 9 + 8 * i][-1])

    fs_rate, signal, l_audio, N, secs, Ts = readWaveFile(waveFileName)
    t = np.linspace(0, secs, signal.size)

    freq = np.arange(2500, 8500, 500)
    freq_target = [3000, 4000, 5000, 6000]
    for i in range(numPackage):
        print(time_start[i], time_end[i])
        start = np.nonzero(t == time_start[i])[0][0]
        end = np.nonzero(t == time_end[i])[0][0]
        n = end - start + 1
        FFT = abs(scipy.fft(signal[start:end]))
        FFT_side = FFT[range(int(n / 2))]
        freqs = scipy.fftpack.fftfreq(n, t[start + 1] - t[start])
        fft_freqs = np.array(freqs)
        freqs_side = freqs[range(int(n / 2))]  # one side frequency range

        indexStart, indexEnd = getStartEndIndex(freq, freqs_side, 500)
        result = getIntegral(indexStart, indexEnd, FFT_side)

        threshold = max(result[5:12]) / 1.9
        if threshold < max_threshold / 4.0:
            threshold = max_threshold / 4.0
        if result.index(max(result)) < 5:
            bit = [0, 0, 0, 0]
        else:
            bit = [1 if result[5] > threshold else 0,
                   1 if result[7] > threshold else 0,
                   1 if result[9] > threshold else 0,
                   1 if result[11] > threshold else 0]

        print(bit)
        plt.plot(freq, result)
        plt.show()


#def findStartSignal():



testSound = 'custom.wav'
# testSound = 'test55.wav'
start_index, time = findFirstIndex(testSound)
print(max_threshold)
getPackage(testSound, start_index, 16, time)
