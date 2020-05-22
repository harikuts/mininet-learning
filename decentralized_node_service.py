#!/usr/bin/python

import socket
import threading
import argparse
import netifaces as ni
import time
import os
import learning_module
from learning_module import Learner

# Parameters
BUFFER_SIZE = 1024
LISTEN_PORT = 13000

# Functions and classes

# Get local (simulated) ethernet IP
# Specifically for Mininet implementation
# https://python-decompiler.com/article/2014-06/how-can-i-get-the-ip-address-of-eth0-in-python
def get_ip_address():
    for interface in ni.interfaces():
        if "eth0" in interface:
            selectInterface = interface
    return ni.ifaddresses(selectInterface)[ni.AF_INET][0]['addr'].encode('ascii', 'ignore')

# MAIN PROGRAM :: SET-UP
parser = argparse.ArgumentParser(description='New node to operate in decentralized setting.')
parser.add_argument( '--netlist', action = 'store', type = str, required = True, \
    help = 'List of other nodes IP addresses and links.')
parser.add_argument('--ip', action = 'store', type = str, default=None, \
    help = 'This nodes IP.')
parser.add_argument( '--datafile', action = 'store', type = str, required = True, \
    help = 'Data file.')
args = parser.parse_args()

# Define LOCALHOST and one-hop NEIGHBORS, assemble NODELIST
try:
    LOCALHOST = args.ip if args.ip is not None else get_ip_address()
    with open(args.netlist, 'r') as f:
        nodeLines = [line.rstrip() for line in f.readlines()]
        neighborLookup = {}
        for nodeLine in nodeLines:
            splits = nodeLine.split(":")
            neighborLookup[splits[0]] = splits[1].split(",")
        NEIGHBORS = neighborLookup[LOCALHOST]
        NODELIST = [LOCALHOST,] + NEIGHBORS
        for line in NODELIST:
            try:
                socket.inet_aton(line)
            except socket.error:
                raise ValueError("One or more IP addresses not valid.")
except:
    print("Failed to resolve host and/or neighbors. Check file or args for errors.")
    print (str(e))
    quit()

print("LOCALHOST:", LOCALHOST)
print("Neighbors:", NEIGHBORS)

# Set up port selection
inboundPhonebook = {}
outboundPhonebook = {}
localID = int(LOCALHOST.split('.')[-1])
for node in NODELIST:
    nodeID =  int(node.split('.')[-1])
    inboundPhonebook[node] = LISTEN_PORT + (localID * 10) + nodeID
    outboundPhonebook[node] = LISTEN_PORT + (nodeID * 10) + localID
print("Inbound Phonebook: " + str(inboundPhonebook))
print("Outbound Phonebook: " + str(outboundPhonebook))

# Listener and Sender classes
# Based on: https://stackoverflow.com/questions/36366774/python-peer-to-peer-chat-sockets

class Listener(threading.Thread):
    # Init
    def __init__(self, port=None):
        threading.Thread.__init__(self)
        self.port = port
    # Run
    def run(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(str(LOCALHOST) + ": Trying to bind to port " + str(self.port))
        try:
            listen_socket.bind((LOCALHOST, self.port))
        except:
            print(str(LOCALHOST) + ": Address taken, resetting and binding")
            listen_socket.close()
            listen_socket.bind((LOCALHOST, self.port))
        print(str(LOCALHOST) + ": Bind complete on port " + str(self.port))
        listen_socket.listen(100)
        # Socket behavior
        conn, addr = listen_socket.accept()
        print(str(LOCALHOST) +  ": Established connection with ", str(addr))
        while True:
            message = conn.recv(BUFFER_SIZE).decode('utf-8')
            message = str(message)
            if message is "<END>":
                print(str(LOCALHOST) +  ": Closing connection from ", str(addr))
                listen_socket.close()
                os.exit(0)
            if message is not "":
                print(str(LOCALHOST) + ": Received " + str(message) + " from port " + str(self.port))

class Sender(threading.Thread):
    # Init
    def __init__(self, address=None, port=None):
        threading.Thread.__init__(self)
        self.address = address
        self.port = port
    # Run
    def run(self):
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            send_socket.connect((self.address, self.port))
        except Exception as e:
            print(str(LOCALHOST) + ": Can't connect to "  + str((self.address, self.port)))
            print(e)
        # Socket behavior
        while True:
            message = "Hello World!"
            try:
                send_socket.send(str.encode(message))
            except Exception as e:
                print(str(LOCALHOST) + ": Unable to send message")
                print(e)
            time.sleep(2.5)
        print(str(LOCALHOST) + ": Completed executions.")
        send_socket.send(str.encode("<END>"))
        send_socket.close()
        os.exit(0)

# Initialize learning model
learner = Learner(LOCALHOST, args.datafile)

for neighbor in NEIGHBORS:
    print(str(LOCALHOST) + ": Starting " + str(neighbor) + " listener")
    listener = Listener(port = inboundPhonebook[neighbor])
    listener.start()
    print("...Done!")

print(str(LOCALHOST) + ": Inbound ports are ready!")

print("Enter 'ok' to continue...")
response = input()
if response.lower() != 'ok':
    print("Exiting.")
    quit()
for neighbor in NEIGHBORS:
    while True:
        try:
            sender = Sender(address = neighbor, port = outboundPhonebook[neighbor])
            break
        except:
            pass
    sender.start()
    