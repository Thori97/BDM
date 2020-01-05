import os
from sklearn.svm import SVC
import numpy as np
from sklearn.externals import joblib
import pyaudio
import time
import threading
import random
import string
import wave
from scipy.io.wavfile import write

clf = joblib.load('svm.pkl.cmp')

samplingrate = 8192
monitorrate = 16#0.1sに1回くらいcheckしよう
CHUNK = 8192


p = pyaudio.PyAudio()

print("monitor start")

stream = p.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = samplingrate,
    input = True,
    frames_per_buffer = CHUNK
)
CHUNK = 512
s = 1.0
RATE = 8192
Hz = RATE
CHUNK = int(RATE*s)
def randomname():
    randlist = [random.choice(string.ascii_letters + string.digits) for i in range(12)]
    return ''.join(randlist)

def worker():
    receive = stream.read(CHUNK+CHUNK//16)
    ret = np.frombuffer(receive, dtype = "int16")[CHUNK//16-1:-1]
    data = np.fft.fft(np.hamming(len(ret))*ret, norm = "ortho")
    data = data[0:CHUNK//2]
    data = np.array([np.abs(data)])
    if clf.predict(data) == [1]:
        print("pashagai emerged!{}".format(random.randint(0, 9)))
        path = os.getcwd() + "/trainincorrect"
        files = os.listdir(path)
        count = len(files)
        fname = randomname()
        np.save(path+ "/" + fname + ".npy", data)
        print(len(data))
        write(path+ "/" + fname + ".wav",RATE,ret)
        print("The data was recorded as incorrect data as {}".format(fname))
    #else:
    #    print("0")
def scheduler(interval, f, wait = True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target = f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

scheduler(1/4, worker, False)
