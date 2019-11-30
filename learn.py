import os
from sklearn.svm import SVC
import numpy as np
from sklearn.externals import joblib

path = os.getcwd()
files = os.listdir(path + "/traincorrect")
cnt1 = 0
cnt2 = 0
X = []
y = []
for file in files:
    if '.npy' in file:
        x = np.load(path + "/traincorrect/" + file)
        #print(file, len(x))
        X.append(x)
        y.append(1)
        cnt1 += 1
path = os.getcwd()
files = os.listdir(path + "/trainincorrect")
for file in files:
    if '.npy' in file:
        x = np.load(path + "/trainincorrect/" + file)
        #print(file, len(x))
        X.append(x)
        y.append(0)
        cnt2 += 1
X = np.array(X)
y = np.array(y)

clf = SVC(C = 1, kernel = 'linear')
#clf = SVC(C = 1.0, kernel = "rbf", gamma = 0.00001)
clf.fit(X, y)

joblib.dump(clf, "svm.pkl.cmp", compress = True)
cnt = cnt1+cnt2
print("{} datas were learned\n{} are pasha\n{} are not pasha".format(cnt, cnt1, cnt2))