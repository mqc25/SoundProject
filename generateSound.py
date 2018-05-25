import wave
import struct
import math

sampleRate = 44100.0 # hertz
duration = 1.0       # seconds
frequency = [440.0, 880, 1660, 3220, 6400]    # hertz

wavef = wave.open('sound.wav','w')
wavef.setnchannels(1) # mono
wavef.setsampwidth(2)
wavef.setframerate(sampleRate)


for freq in frequency:
    for i in range(int(duration * sampleRate)):
        value = int(32767.0*math.cos(freq*math.pi*float(i)/float(sampleRate)))
        data = struct.pack('<h', value)
        wavef.writeframesraw(data)

wavef.writeframes(''.encode())
wavef.close()