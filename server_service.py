#!/usr/bin/python
# Soruce: http://code.activestate.com/recipes/578802-send-messages-between-computers/
# Message Receiver
import os
from socket import *
# import thread

NUM_EPISODES = 8

def process_client(conn, addr):
    print ("Fetching from ", port, "!")
    conn.send(str.encode("<Model>"))
    data = conn.recv(buf).decode('utf-8')
    if data == "<Update>":
        print("Received update from ", addr, ".")

host = ""
ports = [13000, 13001]
buf = 1024
print ("Opening ports...")
addrs = {}
TCPSocks = {}
conns = {}
for port in ports:
    addr = (host, port)
    addrs[port] = addr
    TCPSock = socket(AF_INET, SOCK_STREAM)
    try:
        TCPSock.bind(addr)
    except:
        print("Address taken. Resetting and binding!")
        TCPSock.close()
        TCPSock.bind(addr)
    TCPSock.listen(10)
    conns[port] = TCPSock.accept()
    TCPSocks[port] = TCPSock
    print ("\tPort " + str(port) + " opened!")
# print "Waiting for clients to join..."

# for port in ports:
#     # print("Starting port ", port)
#     conn, addr = TCPSock.accept()

for i in range(NUM_EPISODES):
    print("\nROUND ", i, "\n")
    for port in ports:
        process_client(conns[port][0], conns[port][1])
for port in ports:
    conns[port][0].send(str.encode("<END>"))
print("Press any key to exit")
inp = input()
TCPSocks[port].close()
os._exit(0)