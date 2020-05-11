#!/usr/bin/python
# Soruce: http://code.activestate.com/recipes/578802-send-messages-between-computers/
# Message Receiver
import os
from socket import *
import thread

def enroll_client(conn, addr):
    while True:
        data = conn.recv(buf)
        print "Received message from " + str(addr) + ": " + data
        if data == "exit":
            TCPSocks[port].close()
            break

host = ""
ports = [13000, 13001]
buf = 1024
print "Opening ports..."
addrs = {}
TCPSocks = {}
for port in ports:
    addr = (host, port)
    addrs[port] = addr
    TCPSock = socket(AF_INET, SOCK_STREAM)
    try:
        TCPSock.bind(addr)
    except:
        print "Address taken. Resetting and binding!"
        TCPSock[port].close()
        TCPSock.bind(addr)
    TCPSock.listen(5)
    TCPSocks[port] = TCPSock
    print "\tPort " + str(port) + " opened!"
print "Waiting to receive messages..."
while True:
    for port in ports:
        print("checking ", port)
        conn, addr = TCPSocks[port].accept()
        thread.start_new_thread(enroll_client, (conn, addr))
os._exit(0)