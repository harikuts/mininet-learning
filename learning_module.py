#!/usr/bin/python

import tensorflow as tf
import numpy as np
import argparse
import socket
import pickle
import pdb

SWITCH_PORT = 5000

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
    def __init__(self, ipaddr, datafile=None, modelGenerator=standardNN):
        self.ip = ipaddr
        if datafile is not None:
            self.__read_datafile(datafile)
        pdb.set_trace()

    def __read_datafile(self, df):
        with open(df, 'rb') as rf:
            nodeData = pickle.load(rf)
            self.xtrain = nodeData["xtrain"]
            self.ytrain = nodeData["ytrain"]
            self.xtest = nodeData["xtest"]
            self.ytest = nodeData["ytest"]

### DATA GENERATION ###

# Switch data distribution code
def switch_data_dist(divfilename, dataset):
    print("Switch-enabled data distribution time!")
    with open(divFilename, 'r') as f:
        # Dictionary of IPs and corresponding divisions
        divInfo = {}
        # List of IPs in order to determine which blocks of data
        IPlist = []
        # IP data allocations
        IPdata = {}
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
        # Per each IP address
        for IP in IPlist:
            print("Generating data for " + str(IP))
            # Find position of IP address to determine the beginning/end of the division
            ind = IPlist.index(IP)
            if ind > 0:
                prevDivs = [divInfo[prevIP] for prevIP in IPlist[0:(ind)]]
                print("prevDivs", prevDivs)
                rangeBeginning = sum(prevDivs)
            else:
                rangeBeginning = 0
            rangeEnd = divInfo[IP] + rangeBeginning
            # Set dictionary for this IP
            thisNode = {}
            # Grab data from mnist module
            (trainX, trainY), (testX, testY) = dataset.load_data()
            trainX, testX = trainX / 255.0, testX / 255.0
            # Map divisions onto training data
            trainBeginning = int(rangeBeginning * len(trainX))
            trainEnd = int(rangeEnd * len(trainX))
            # print(type(trainEnd))
            thisNode["xtrain"] = trainX[trainBeginning:trainEnd]
            thisNode["ytrain"] = trainY[trainBeginning:trainEnd]
            # Map divisions onto testing data
            testBeginning = int(rangeBeginning * len(testX))
            testEnd = int(rangeEnd * len(testX))
            thisNode["xtest"] = testX[testBeginning:testEnd]
            thisNode["ytest"] = testY[testBeginning:testEnd]
            # Set data groups in a dictionary
            IPdata[IP] = thisNode
        # Set up files for each IP
        for IP in IPlist:
            filename = str(IP) + "-data.pkl"
            wf = open(filename, 'wb')
            pickle.dump(IPdata[IP], wf)
                

        

if __name__ == "__main__":
    print("Generating data files based on division file...")
    parser = argparse.ArgumentParser(description='Run as main() to enable data distribution from switch.')
    parser.add_argument( '--div', action = 'store', type = str, required = True, \
        help = 'IP addresses and divisions.')
    # parser.add_argument( '--ip', action = 'store', type = str, required = True, \
    #     help = 'Target switch IP address.')
    args = parser.parse_args()
    divFilename = args.div
    dataset = tf.keras.datasets.mnist
    switch_data_dist(divFilename, dataset)