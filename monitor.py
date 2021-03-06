import os
from sklearn.svm import SVC
import numpy as np
from sklearn.externals import joblib
import pyaudio
import time
import threading
import random
import serial

clf = joblib.load('svm.pkl.cmp')
#ser = serial.Serial("/dev/tty.usbmodem1413", 115200)
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


count = 0
freq = 6#1秒に何回とるか
rateth = 0.5#なん%OKならパシャ判定か
th = freq*rateth
q = np.zeros(freq)#結果格納 長さがfreqである必要はない


def worker():
    receive = stream.read(CHUNK+CHUNK//16)
    ret = np.frombuffer(receive, dtype = "int16")[CHUNK//16-1:-1]
    data = np.fft.fft(np.hamming(len(ret))*ret, norm = "ortho")
    data = data[0:CHUNK//2]
    data = np.array([np.abs(data)])
    global count
    global freq
    global th
    global q
    count+=1
    if clf.predict(data) == [1]:
        #print(1)
        q[count%freq] = 1
        #print("pashagai emerged!{}".format(random.randint(0, 9)))
        #ser.write(chr(119).encode())
        #time.sleep(1)
        #ser.write(chr(1).encode())
    else:
        #print(0)
        q[count%freq] = 0
    if np.sum(q)>th:
        print("pashagai emerged!{}".format(random.randint(0, 9)))
        q = np.zeros(freq)
        #ser.write(chr(119).encode())
        #time.sleep(1)
        #ser.write(chr(1).encode())
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
        #global count
        #if count > 100:
        #    break
#start = time.time()
scheduler(1/freq, worker, False)
#end = time.time()
#print("{} times in 1s".format(100/(end-start)))