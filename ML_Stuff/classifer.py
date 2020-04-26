
import tensorflow as tf
from keras.layers import TimeDistributed, RepeatVector, LSTM, Dense, Dropout
from keras.models import Sequential
import numpy as np

def build_model(weights_file):
    model = Sequential()
    model.add(LSTM(10, activation='relu', input_shape=(4,1)))
    model.add(RepeatVector(4))
    model.add(LSTM(10, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(1)))
    model.compile(optimizer='adam', loss='mse')
    model.load_weights(weights_file)
    return model

def get_prediction(data, model):
    return model.predict(data)

def find_anomalies(real, pred):
    print("P: ", type(pred))
    print("R: ", type(real))
    mae_of_predictions = np.squeeze(np.max(np.square(pred-real), axis=1))
    mae_threshold = np.mean(mae_of_predictions) + np.std(mae_of_predictions)
    actual = np.where(mae_of_predictions > mae_threshold)[0]
    return actual