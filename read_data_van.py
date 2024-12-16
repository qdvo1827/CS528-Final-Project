import serial
import time
import csv
import pandas as pd
import pickle
import os
import re
import warnings
import datetime
import pathlib
import glob
import numpy as np
import pandas as pd
import joblib
import pickle
from scipy import signal
from sklearn import metrics
from sklearn import tree, svm

from sklearn import tree, metrics
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
from scipy.signal import butter, filtfilt, find_peaks
from sklearn.tree import DecisionTreeClassifier,export_graphviz
from sklearn.model_selection import train_test_split

from djitellopy import Tello
import keyboard


def remove_noise(data,sampling_rate):

    # Low pass filter
    cutoff = 5 # Hz
    order = 2
    b, a = butter(order, cutoff/(sampling_rate/2), btype='lowpass')
    data.iloc[:,0] = filtfilt(b, a, data.iloc[:,0])
    data.iloc[:,1] = filtfilt(b, a, data.iloc[:,1])
    data.iloc[:,2] = filtfilt(b, a, data.iloc[:,2])

    return data

# tello = Tello()
# tello.connect()
# tello.takeoff()

count = 0

with open('./van_svc_2.pkl', 'rb') as f:
    classifier = pickle.load(f)

# with open('../classifier.pkl', 'rb') as f:
#     classifier = pickle.load(f)

# t_end = time.time() + 1
#     while time.time() < t_end:
#         pass

tello = Tello()
tello.connect()
tello.takeoff()

with serial.Serial(port='/dev/tty.usbserial-14330', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0) as ser:
    print("START!")
    time.sleep(1)
    while True:
        try:  
            accel_x = []
            accel_y = []
            accel_z = []
            gyro_x = []
            gyro_y = []
            gyro_z = []
            count = 0
            t_end = time.time() + 4
            print("START READING DATA")
            while time.time() < t_end:
                line = ser.readline()
                if line:
                    count += 1
                    line = line.decode()
                    #print(line)
                    # f.write(str(count) + ", "+ line)
                    line = line.replace(' ', '')
                    data = line.split(',')
                    if len(data) == 6:
                        data[5] = data[5].replace('\r\n', '')
                        accel_x.append(float(data[0]))
                        accel_y.append(float(data[1]))
                        accel_z.append(float(data[2]))

                        gyro_x.append(float(data[3]))
                        gyro_y.append(float(data[4]))
                        gyro_z.append(float(data[5]))
                        print(f"{data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}")
                    print(f"{count}, {len(data)}")

            dict = {'accel_x': accel_x, 'accel_y': accel_y, 'accel_z': accel_z, 'gyro_x': gyro_x, 'gyro_y': gyro_y, 'gyro_z': gyro_z}
            data = pd.DataFrame(dict)
            #data = remove_noise(data, 100)
            print(len(data))
            data = data.iloc[-400:,:]

            data = data[['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z']].to_numpy()
            #data = data[['accel_x', 'accel_y', 'accel_z']].to_numpy()

            # Normalize data
            data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

            # Populate lists with normalized data and labels
            features = []
            features.append(data.flatten())
            pred = classifier.predict(np.array(features))


            print(f"PREDICTION: {pred}")
            if pred == "front":
                tello.move_forward(30)
            elif pred == "back":
                tello.move_back(30)
            elif pred == "up":
                tello.move_up(30)
            elif pred == "down":
                tello.move_down(30)
            elif pred == "right":
                tello.move_right(30)
            elif pred == "left":
                tello.move_left(30)
            elif pred == "clockwise":
                tello.rotate_clockwise(15)
            elif pred == "counter_clockwise":
                tello.rotate_counter_clockwise(15)
            time.sleep(3)
        except KeyboardInterrupt:
            print("DONE!")
            break

tello.land()

    
# ser.close()


