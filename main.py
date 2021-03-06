from Encoding import *
from test import *
from HammingCode import *
import base64
import zlib

freq_range = [3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500]
zero_freq = [3000]
start_freq = [10000]

def createWavFile(waveFileName,bits):
    waveFinal = generateFullSignal(bits, start_freq, 0.04, freq_range, zero_freq, 0.16, 250)
    createWaveFormFile('custom.wav', waveFinal)

def decodeMsg(waveFileName):
    mag, phase, freq = doFFT(waveFileName, 0.04)
    mag, phase, freq = findSignal(mag, phase, freq, start_freq[0], 250)
    #freq_target = [3000]
    #freq_target += list(range(5000,9000,500))
    freq_target = freq_range
    #print(freq_target)
    freq_list = list(range(2500, 10500, 250))
    msg = doIntegral(mag, phase, freq, freq_list, 8, 250, freq_target)
    decodeMsg = []
    for singleMsg in msg:
        num = 0
        for bit in singleMsg:
            num = (num << 1) | bit
        decodeMsg.append(num)
    #print(decodeMsg)
    return decodeMsg

def errorChecking(a,b):
    errorCount = 0
    errorIndex = []
    for i in range(len(a)):
        if a[i] != b[i]:
            errorCount += 1
            errorIndex.append(i)
    if errorCount == 0:
        print("No Error")
    else:
        print("Error:")
        for i in errorIndex:
            print(i, a[i], b[i])

def textToSequence(text):
    seq = [ord(c) for c in text]
    return seq

def sequenceToText(seq):
    text = ''.join(chr(i) for i in seq)
    return text

def createWavFromMsg(text,waveFileName):
    seq = textToSequence(text)
    for i in range(len(seq)):
        seq[i] = generateHammingCode(seq[i])
    print(seq)
    createWavFile(waveFileName,seq)

def decodeWavToMsg(waveFileName):
    estimateMsg = decodeMsg(waveFileName)
    for i in range(len(estimateMsg)):
        estimateMsg[i] = decodeHamingCode(estimateMsg[i])
    #print(estimateMsg)
    text = sequenceToText(estimateMsg)
    return text

# bitSequence = [13, 25, 50, 75, 100, 125, 150, 175, 200, 225, 255 ,0 , 128, 254,12,64,57,135,179,243]
# ##createWavFile('custom.wav',bitSequence)

# testSeq = textToSequence("Hello Word")
# testMsg = sequenceToText(testSeq)
# print(testSeq)
# print(testMsg)

# DecodeMsg = decodeMsg('test12.wav')
# print(bitSequence)
# print(DecodeMsg)
# errorChecking(bitSequence,DecodeMsg)

sendMsg = 'test MSG right now should not be any ISSUE leftover.'
#
print(sendMsg)
createWavFromMsg(sendMsg,'custom.wav')


decodeFile = 'final5.wav'
textMsg = decodeWavToMsg(decodeFile)
print(sendMsg)
print(textMsg)
