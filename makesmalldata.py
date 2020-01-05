import os
import numpy as np

path = os.getcwd()
files = os.listdir(path + "/traincorrect/")
for file in files:
    if '.npy' in file:
        x = np.load(path + "/traincorrect/" + file)
        x*=0.3
        fname=file.replace(".npy", "03.npy")
        np.save(path + "/traincorrect/"+fname, x)