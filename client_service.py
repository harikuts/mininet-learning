#!/usr/bin/python
import socket
import sys
import os
import argparse
import traceback
import time
import tqdm
from threading import Thread

SEPARATOR = "<SEP>"
BUFFER_SIZE = 4096

"""
This code is based on code from
https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python.
"""

# parser = argparse.ArgumentParser(description='Run as main() to enable data distribution from switch.')
# parser.add_argument( '--div', action = 'store', type = str, required = True, \
#     help = 'IP addresses and divisions.')

def client_process(self_ip, neighbor_ip, base_path):
    # Get host and port information
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = neighbor_ip
    port = 8000
    buffer_size = 4096
    try:
        soc.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()
    # print("Please enter 'quit' to exit.")
    # message = input(">>> ")
    # while message != 'quit':
    #     soc.sendall(message.encode("utf8"))
    #     # Null
    #     print("Delivering...")
    #     if soc.recv(5120).decode("utf8") == "-":
    #         pass
    #     print("\tSent!")
    #     message = input(">>> ")
    # soc.send(b'--quit--')
    base_path = "/" + base_path.strip("/")
    outbox_path = base_path + "/outbox"
    outfile = outbox_path + "/sample.txt"
    while True:
        # message = "hi"
        # soc.sendall(message.encode("utf8"))
        # print("Delivering...")
        # if soc.recv(5120).decode("utf8") == "-":
        #     pass
        # print("\tSent!")

        # Sending mechanism from: 
        # https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
        if os.path.exists(outfile):
            send_file(soc, outfile)
        time.sleep(10)

# Sending mechanism from: 
# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
def send_file(soc, filename):
    filesize = os.path.getsize(filename)
    soc.send(f"{filename}{SEPARATOR}{filesize}".encode())
    # Wait for acknowledgment
    if soc.recv(5120).decode() == "^":
        pass
    # Progress bar
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", \
            unit="B", unit_scale=True, unit_divisor=1024)
    # Actually read from file
    with open(filename, "rb") as f:
        for _ in progress:
            # Read bytes; if none left, then break
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            # Send bytes
            soc.sendall(bytes_read)
            # Wait for acknowledgment
            if soc.recv(5120).decode() == "-":
                pass
            # Update progress bar
            progress.update(len(bytes_read))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run client service.')
    parser.add_argument( '--ip', action = 'store', type = str, required = True, \
        help = 'Local IP address.')
    parser.add_argument( '--net', action = 'store', type = str, required = True, \
        help = 'File of network links with each line in the format <LOCAL_IP:NEIGHBOR_IP,NEIGHBOR_IP,etc.>.')
    parser.add_argument( '--path', action = 'store', type = str, required = True, \
        help = 'Path to base directory.')
    args = parser.parse_args()

    # Process netlinks file to get neighbors
    net_lookup = {}
    with open(args.net) as f:
        for line in f.readlines():
            line = line.strip()
            info = line.split(':')
            net_lookup[info[0]] = info[1].split(',')
    
    print ("Neighbors: " + str(net_lookup[args.ip]))
    for neighbor_ip in net_lookup[args.ip]:
        print (neighbor_ip)
        try:
            Thread(target=client_process, args=(args.ip, neighbor_ip, args.path)).start()
            print("\tNeighbor thread started.")
        except:
            print("\tCan't start thread.")
            traceback.print_exc()