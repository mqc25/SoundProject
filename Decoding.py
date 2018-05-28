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

freq_oneside, FFT_side = getFFTfromFile('test5.wav')
freq = np.arange(0,13000,250)

indexStart,indexEnd = getStartEndIndex(freq,freq_oneside,500)
result = getIntegral(indexStart,indexEnd,FFT_side)

plt.plot(freq,result)
plt.show()
