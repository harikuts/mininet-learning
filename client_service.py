#!/usr/bin/python
# Source: http://code.activestate.com/recipes/578802-send-messages-between-computers/
# Message Sender
import os
from socket import *
import argparse
parser = argparse.ArgumentParser(description='Send a message to a target machine.')
parser.add_argument( '--target', action = 'store', type = str, help = 'Target IP address.' )
args = parser.parse_args()

host = args.target # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = raw_input("Enter message to send or type 'exit': ")
    UDPSock.sendto(data, addr)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)