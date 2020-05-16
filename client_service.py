#!/usr/bin/python
# Source: http://code.activestate.com/recipes/578802-send-messages-between-computers/
# Message Sender
import os
from socket import *
import argparse
parser = argparse.ArgumentParser(description='Send a message to a target machine.')
parser.add_argument( '--target', action = 'store', type = str, help = 'Target IP address.' )
parser.add_argument( '--port', action='store', type = int, help = 'Target IP port.')
args = parser.parse_args()

RECV_BUFFER = 1024

host = args.target # set to IP address of target computer
port = args.port # set port
addr = (host, port)
TCPSock = socket(AF_INET, SOCK_STREAM)
TCPSock.connect(addr)
while True:
    data = TCPSock.recv(RECV_BUFFER).decode('utf-8')
    # Check if this is model information
    if data == "<Model>":
        print(port, ": Performing some algorithm.")
        TCPSock.send(str.encode("<Update>"))
        print(port, ": Sent update.")
    elif data == "<END>":
        break
# TCPSock.close()
os._exit(0)