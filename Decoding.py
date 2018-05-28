import generateSound
import numpy as np
from fft import *
import matplotlib.pyplot as plt

THRESH_HOLD = 1e6

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

freq = np.arange(2500,13000,250)






# freq_oneside, FFT_side = getFFTfromFile('test6.wav')
# indexStart,indexEnd = getStartEndIndex(freq,freq_oneside,500)
# result = getIntegral(indexStart,indexEnd,FFT_side)




time_chunk, freq_oneside_chunk, FFT_side_chunk = performFFTinChunk('custom.wav',0.04)
freq = [7000]
result_chunk = []

time_start = []

start_index = None

for i in range(len(freq_oneside_chunk)):
    indexStart,indexEnd = getStartEndIndex(freq,freq_oneside_chunk[i],500)
    resultTemp = getIntegral(indexStart,indexEnd,FFT_side_chunk[i])
    result_chunk.append(resultTemp)
    time_start.append(time_chunk[i][0])
    if resultTemp[0] > THRESH_HOLD:
        start_index = i
        break

print("start_index",start_index)

time_start1 = time_chunk[start_index+2][0]
time_end1 = time_chunk[start_index+5][-1]

time_start2 = time_chunk[start_index+6][0]
time_end2 = time_chunk[start_index+9][-1]

print("time_start1",time_start1)
print("time_start2",time_start2)

print("time_end1",time_end1)
print("time_end2",time_end2)



fs_rate, signal, l_audio, N, secs, Ts = readWaveFile('custom.wav')

# t = scipy.arange(0, secs, Ts)  # time vector as scipy arange field / numpy.ndarray
t = np.linspace(0, secs, signal.size)

start_index1 = np.nonzero(t == time_start1)[0][0]
end_index1 = np.nonzero(t == time_end1)[0][0]
n = end_index1 - start_index1 + 1
FFT1 = abs(scipy.fft(signal[start_index1:end_index1]))
FFT_side1 = FFT1[range(int(n/ 2))]
freqs1 = scipy.fftpack.fftfreq(n, t[start_index1+1] - t[start_index1])
fft_freqs1 = np.array(freqs1)
freqs_side1 = freqs1[range(int(n / 2))]  # one side frequency range


start_index2 = np.nonzero(t == time_start2)[0][0]
end_index2 = np.nonzero(t == time_end2)[0][0]
n = end_index2 - start_index2 + 1
FFT2 = abs(scipy.fft(signal[start_index2:end_index2]))
FFT_side2 = FFT2[range(int(n/ 2))]
freqs2 = scipy.fftpack.fftfreq(n, t[start_index1+1] - t[start_index1])
fft_freqs2 = np.array(freqs2)
freqs_side2 = freqs2[range(int(n / 2))]  # one side frequency range

freq = np.arange(2500,6500,500)



indexStart, indexEnd = getStartEndIndex(freq, freqs_side1, 500)
result1 = getIntegral(indexStart,indexEnd,FFT_side1)

indexStart, indexEnd = getStartEndIndex(freq, freqs_side2, 500)
result2 = getIntegral(indexStart,indexEnd,FFT_side2)

# print(start_index)
# # # plt.plot(time_start,result_chunk)
# # # plt.show()

plt.plot(freq,result1)
plt.show()
plt.plot(freq,result2)
plt.show()

