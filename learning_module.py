#!/usr/bin/python

import tensorflow as tf
import numpy as np
import socket

def standardNN():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28,28)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
    ])
    loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])
    return model

class Learner:
    def __init__(self, ipaddr, divFilename, modelGenerator=standardNN):
        self.ip = ipaddr
        datasetSelect = tf.keras_datasets.mnist
        self.__grab_data(divFilename, datasetSelect)
        print(str(self.ip) + ": range division @ " + str(self.data))
    
    def __get_data(self, divFilename, dataset):
        with open(divFilename, 'r') as f:
            # Dictionary of IPs and corresponding divisions
            divInfo = {}
            # List of IPs in order to determine which blocks of data
            IPlist = []
            # Read lines
            lines = [line.rstrip() for line in f.readlines()]
            for line in lines:
                # Check to see that IP address and division are valid
                try:
                    info = line.split(":")
                    socket.inet_aton(info[0])
                    info[1] = float(info[1])
                    assert info[1] <= 1.0 and info[1] > 0.0
                except:
                    raise ValueError(str(info) + \
                        " is not a valid IP address and/or division.")
                divInfo[info[0]] = info[1]
                IPlist.append(info[0])
            # Find position of IP address to determine the beginning/end of the division
            ind = IPlist.index(self.ip)
            if ind > 0:
                prevDivs = [divInfo[prevIP] for prevIP in IPlist[0:(ind)]]
                print("prevdivs", prevDivs)
                rangeBeginning = sum(prevDivs)
            else:
                rangeBeginning = 0
            rangeEnd = divInfo[self.ip] + rangeBeginning
           
            