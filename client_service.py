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

host = args.target # set to IP address of target computer
port = args.port # set port
addr = (host, port)
TCPSock = socket(AF_INET, SOCK_STREAM)
TCPSock.connect(addr)
while True:
    data = raw_input("Enter message to send or type 'exit': ")
    TCPSock.send(data)
    if data == "exit":
        break
TCPSock.close()
os._exit(0)