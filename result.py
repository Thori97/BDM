import os
from sklearn.svm import SVC
import numpy as np
from sklearn.externals import joblib

clf = joblib.load('svm.pkl.cmp')
print("model loaded")
path = os.getcwd()
files = os.listdir(path + "/testcorrect")
for file in files:
    if '.npy' in file:
        x = np.load(path + "/testcorrect/" + file)
        x = np.array([x])
        print("This is pashaon, {}  predicted {}".format(file, clf.predict(x)))

files = os.listdir(path + "/testincorrect")
for file in files:
    if '.npy' in file:
        x = np.load(path + "/testincorrect/" + file)
        x = np.array([x])
        print("This is not pashaon, {}  predicted {}".format(file, clf.predict(x)))