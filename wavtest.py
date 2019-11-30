import pyaudio
import wave
import numpy as np
import time
import matplotlib.pyplot as plt
import os
import random
import string

def randomname():
    randlist = [random.choice(string.ascii_letters + string.digits) for i in range(12)]
    return ''.join(randlist)

from scipy.io.wavfile import write

CHUNK = 512
s = 1.0
RATE = 8192
Hz = RATE
CHUNK = int(RATE*s)

p = pyaudio.PyAudio()


print("3")
time.sleep(1)
print("2")
time.sleep(1)
print("1")
time.sleep(1)
print("play")

stream = p.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = RATE,
    input = True,
    frames_per_buffer = CHUNK
)


receive = stream.read(CHUNK+CHUNK//16)
ret = np.frombuffer(receive, dtype = "int16")[CHUNK//16-1:-1]

stream.close()
print("end")

data = np.fft.fft(np.hamming(len(ret))*ret, norm = "ortho")
data = np.abs(data)
data = data[0:CHUNK//2]
print(len(data))


x = np.linspace(0, RATE/2, CHUNK/2)
t = np.linspace(0, s, CHUNK)

fig = plt.figure()

axL = fig.add_subplot(1, 2, 1)
axL.plot(t, ret)
axL.set_ylim([-1*2**15, 2**15])
axL.set_title("wave")

axR = fig.add_subplot(1, 2, 2)
axR.plot(x, data)
axR.set_title("spector")

plt.show()

print("If you save as a Correct Answer Data → t")
print("If you save as a Incorrect Data      → f")
print("If you save as a Correct Test Data   → a")
print("If you save as a Incorrect Test Data → b")
print("If you don't save Data               → n or others")
char = input()

if char == "t" or char == "T":
    path = os.getcwd() + "/traincorrect"
    files = os.listdir(path)
    count = len(files)
    fname = randomname()
    np.save(path+ "/" + fname + ".npy", data)
    path2 = os.getcwd() + "/traincorrect"
    write(path2+ "/" + fname + ".wav",RATE,ret)
    print("The data was recorded as correct data as {}".format(fname))

elif char == "f" or char == "F":
    path = os.getcwd() + "/trainincorrect"
    files = os.listdir(path)
    count = len(files)
    fname = randomname()
    np.save(path+ "/" + fname + ".npy", data)
    path2 = os.getcwd() + "/trainincorrect"
    write(path2+ "/" + fname + ".wav",RATE,ret)
    print("The data was recorded as incorrect data as {}".format(fname))
elif char == "n" or char == "N":
    print("The data was discarded")

elif char == 'a' or char == "A":
    path = os.getcwd() + "/testcorrect"
    fname = randomname()
    np.save(path+ "/" + fname + ".npy", data)
    path2 = os.getcwd() + "/testcorrect"
    write(path2+ "/" + fname + ".wav",RATE,ret)
    print("The data was saved as correct test data as {}".format(fname))

elif char == 'b' or char == "B":
    path = os.getcwd() + "/testincorrect"
    fname = randomname()
    np.save(path+ "/" + fname + ".npy", data)
    path2 = os.getcwd() + "/testincorrect"
    write(path2+ "/" + fname + ".wav",RATE,ret)
    print("The data was saved as incorrect test data as {}".format(fname))

else:
    print("It can be a mistake, but the data was discarded")
