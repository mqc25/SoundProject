from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def readWaveFile(waveFileName):
    fs_rate, signal = wavfile.read(waveFileName)
    l_audio = len(signal.shape)
    if l_audio == 2:
        signal = signal.sum(axis=1) / 2
    N = signal.shape[0]
    secs = N / float(fs_rate)
    Ts = 1.0 / fs_rate  # sampling interval in time

    print("Frequency sampling", fs_rate)
    print("Channels", l_audio)
    print("Complete Samplings N", N)
    print("secs", secs)
    print("Timestep between samples Ts", Ts)

    return fs_rate, signal, l_audio, N, secs, Ts

def performFFTonFile(waveFileName):
    fs_rate, signal, l_audio, N, secs, Ts = readWaveFile(waveFileName)

    #t = scipy.arange(0, secs, Ts)  # time vector as scipy arange field / numpy.ndarray
    t = np.linspace(0,secs,signal.size)
    FFT = abs(scipy.fft(signal))
    FFT_side = FFT[range(int(N / 2))]  # one side FFT range
    freqs = scipy.fftpack.fftfreq(signal.size, t[1] - t[0])
    fft_freqs = np.array(freqs)
    freqs_side = freqs[range(int(N / 2))]  # one side frequency range
    fft_freqs_side = np.array(freqs_side)

    return t, signal, FFT, FFT_side, freqs, fft_freqs, freqs_side, fft_freqs_side

def plotFFT(t, signal, FFT, FFT_side, freqs, fft_freqs, freqs_side, fft_freqs_side):
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    plt.plot(t, signal, "g")  # plotting the signal
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.grid(True)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    ax2 = fig.add_subplot(312)
    plt.plot(freqs, FFT, "r")  # plotting the complete fft spectrum
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.grid(True)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count dbl-sided')

    ax3 = fig.add_subplot(313)
    plt.plot(freqs_side, abs(FFT_side), "b")  # plotting the positive fft spectrum
    ax3.xaxis.set_minor_locator(AutoMinorLocator())
    ax3.grid(True)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count single-sided')
    plt.show()

def getFFTfromFile(waveFileName):
    t, signal, FFT, FFT_side, freqs, fft_freqs, freqs_side, fft_freqs_side = performFFTonFile(waveFileName)
    return freqs_side, abs(FFT_side)


#t, signal, FFT, FFT_side, freqs, fft_freqs, freqs_side, fft_freqs_side = performFFTonFile('custom.wav')
#plotFFT(t, signal, FFT, FFT_side, freqs, fft_freqs, freqs_side, fft_freqs_side)

