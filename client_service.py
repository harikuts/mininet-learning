#!/usr/bin/python
import socket
import sys
import argparse

"""
This code is based on code from
https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python.
"""

# parser = argparse.ArgumentParser(description='Run as main() to enable data distribution from switch.')
# parser.add_argument( '--div', action = 'store', type = str, required = True, \
#     help = 'IP addresses and divisions.')

def client_process(neighbor_ip):
    # Get host and port information
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "10.0.0.1"
    port = 8000
    try:
        soc.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()
    print("Please enter 'quit' to exit.")
    message = input(">>> ")
    while message != 'quit':
        soc.sendall(message.encode("utf8"))
        # Null
        print("Delivering...")
        if soc.recv(5120).decode("utf8") == "-":
            pass
        print("\tSent!")
        message = input(">>> ")
    soc.send(b'--quit--')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run client service.')
    parser.add_argument( '--ip', action = 'store', type = str, required = True, \
        help = 'Local IP address.')
    parser.add_argument( '--net', action = 'store', type = str, required = True, \
        help = 'File of network links with each line in the format <LOCAL_IP:NEIGHBOR_IP,NEIGHBOR_IP,etc.>.')
    args = parser.parse_args()

    # Process netlinks file to get neighbors
    net_lookup = {}
    with open(args.net) as f:
        for line in f.readlines():
            line = line.strip()
            info = line.split(':')
            net_lookup[info[0]] = info[1].split(',')
    
    print (net_lookup[args.ip])

    client_process("10.0.0.1")