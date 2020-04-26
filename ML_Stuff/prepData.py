from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
import numpy as np

def scaler(data):
    data = np.array(data).reshape(-1,1)
    scaler = joblib.load("C:/Users/John Q-G/Documents/GitHub/scaler.save")
    return scaler.transform(data)

def define_context(data, n):
    x = []
    i = 0
    while(i+n) < len(data):
        x.append(data[i:i+n])
        i+=1
        
    return x

def final_prep(data, shift, features):
    return np.array(data).reshape(len(data), shift, features)