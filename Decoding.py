import generateSound
import numpy as np
from fft import *
import matplotlib.pyplot as plt


def getStartEndIndex(freq_list, freq_fft, bandwidth):
    countStart = 0
    countEnd = 0

    indexStart = []
    indexEnd = []
    for i in range(len(freq_fft)):
        if countStart < len(freq_list) and freq_fft[i] > freq_list[countStart] :
            indexStart.append(i)
            countStart += 1


        if(freq_fft[i] > freq_list[countEnd] + bandwidth):
            indexEnd.append(i)
            countEnd += 1
            if countEnd == len(freq_list):
                return indexStart, indexEnd

def getIntegral(indexStart,indexEnd,FFT):
    value = []
    for i in range(len(indexStart)):
        value.append(sum(FFT[indexStart[i]:indexEnd[i]]))
    return value


#freq_oneside, FFT_side = getFFTfromFile('test6.wav')







# freq_oneside, FFT_side = getFFTfromFile('test6.wav')
# indexStart,indexEnd = getStartEndIndex(freq,freq_oneside,500)
# result = getIntegral(indexStart,indexEnd,FFT_side)



max_threshold = 0

def findFirstIndex(waveFileName):
    time_chunk, freq_oneside_chunk, FFT_side_chunk = performFFTinChunk(waveFileName, 0.04)
    freq = [9000]
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




def getPackage(waveFileName,start_i, numPackage, time):
    time_start = []
    time_end = []
    for i in range(numPackage):
        time_start.append(time[start_i+2 + 4*i][0])
        time_end.append(time[start_i + 5 + 4*i][-1])


    fs_rate, signal, l_audio, N, secs, Ts = readWaveFile(waveFileName)
    t = np.linspace(0, secs, signal.size)

    freq = np.arange(1500, 8500, 500)
    freq_target = [3000,4000,5000,6000]
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

        threshold = max(result)/ 3
        if threshold < max_threshold/4.0:
            threshold = max_threshold/4.0
        if result.index(max(result)) == 1:
            bit = [0,0,0,0]
        else:
            bit = [ 1 if result[7] > threshold else 0,
                    1 if result[9] > threshold else 0,
                    1 if result[11] > threshold else 0,
                    1 if result[13] > threshold else 0 ]

        print(bit)
        plt.plot(freq, result)
        plt.show()
#testSound = 'custom.wav'
testSound = 'test28.wav'
start_index, time = findFirstIndex(testSound)
print(max_threshold)
getPackage(testSound,start_index,16,time)

# print("start_index",start_index)
#
# time_start1 = time_chunk[start_index+2][0]
# time_end1 = time_chunk[start_index+5][-1]
#
# time_start2 = time_chunk[start_index+6][0]
# time_end2 = time_chunk[start_index+9][-1]
#
# print("time_start1",time_start1)
# print("time_start2",time_start2)
#
# print("time_end1",time_end1)
# print("time_end2",time_end2)

#
#
# fs_rate, signal, l_audio, N, secs, Ts = readWaveFile(testSound)
#
# # t = scipy.arange(0, secs, Ts)  # time vector as scipy arange field / numpy.ndarray
# t = np.linspace(0, secs, signal.size)
#
# start_index1 = np.nonzero(t == time_start1)[0][0]
# end_index1 = np.nonzero(t == time_end1)[0][0]
# n = end_index1 - start_index1 + 1
# FFT1 = abs(scipy.fft(signal[start_index1:end_index1]))
# FFT_side1 = FFT1[range(int(n/ 2))]
# freqs1 = scipy.fftpack.fftfreq(n, t[start_index1+1] - t[start_index1])
# fft_freqs1 = np.array(freqs1)
# freqs_side1 = freqs1[range(int(n / 2))]  # one side frequency range
#
#
# start_index2 = np.nonzero(t == time_start2)[0][0]
# end_index2 = np.nonzero(t == time_end2)[0][0]
# n = end_index2 - start_index2 + 1
# FFT2 = abs(scipy.fft(signal[start_index2:end_index2]))
# FFT_side2 = FFT2[range(int(n/ 2))]
# freqs2 = scipy.fftpack.fftfreq(n, t[start_index1+1] - t[start_index1])
# fft_freqs2 = np.array(freqs2)
# freqs_side2 = freqs2[range(int(n / 2))]  # one side frequency range
#
# freq = np.arange(2500,6500,500)
#
#
#
# indexStart, indexEnd = getStartEndIndex(freq, freqs_side1, 500)
# result1 = getIntegral(indexStart,indexEnd,FFT_side1)
#
# indexStart, indexEnd = getStartEndIndex(freq, freqs_side2, 500)
# result2 = getIntegral(indexStart,indexEnd,FFT_side2)
#
# # print(start_index)
# # # # plt.plot(time_start,result_chunk)
# # # # plt.show()
#
# plt.plot(freq,result1)
# plt.show()
# plt.plot(freq,result2)
# plt.show()

