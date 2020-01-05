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
#monitorrate = 16#0.1sに1回くらいcheckしよう
CHUNK = 8192


p = pyaudio.PyAudio()

print("monitor start")

def callback(in_data, frame_count, time_info, status):
    #out_data = in_data
    return (in_data, pyaudio.paContinue)

stream = p.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = samplingrate,
    input = True,
    frames_per_buffer = CHUNK,
    stream_callback=callback
)
"""
def worker():
    receive = stream.read(CHUNK+CHUNK//16)
    ret = np.frombuffer(receive, dtype = "int16")[CHUNK//16-1:-1]
    data = np.fft.fft(np.hamming(len(ret))*ret, norm = "ortho")
    data = data[0:CHUNK//2]
    data = np.array([np.abs(data)])
    if clf.predict(data) == [1]:
        #print("pashagai emerged!{}".format(random.randint(0, 9)))
        ser.write(chr(119).encode())
        time.sleep(1)
        ser.write(chr(1).encode())
        print("a")
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

scheduler(1/4, worker, False)"""

count = 0
stream.start_stream()
st = time.time()
while time.time() < st + 2.0:
    print("")
start = time.time()
repeats = 10
for i in range(0, repeats):
    receive = stream.read(CHUNK+CHUNK//16)
    ret = np.frombuffer(receive, dtype = "int16")[CHUNK//16-1:-1]
    data = np.fft.fft(np.hamming(len(ret))*ret, norm = "ortho")
    data = data[0:CHUNK//2]
    data = np.array([np.abs(data)])
    if clf.predict(data) == [1]:
        #print("pashagai emerged!{}".format(random.randint(0, 9)))
        #ser.write(chr(119).encode())
        #time.sleep(1)
        #ser.write(chr(1).encode())
        count+=1
    else:
        count+=1
end = time.time()
print("{}s for 1 time".format((end-start)/repeats))