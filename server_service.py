#!/usr/bin/python
import socket
import sys
import os
import traceback
from threading import Thread
import argparse
import tqdm

SEPARATOR = "<SEP>"
BUFFER_SIZE = 4096

"""
This code is based on code from
https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python.
"""

def main():
    start_server('127.0.0.1')

class Server:
    # Constructor
    def __init__(self, ip_addr, net_file, storage_path):
        self.ip_addr = ip_addr
        self.net_file = net_file
        self.storage_path = storage_path
    # Server process
    def start_server(self):
        # Set host and port information
        host = self.ip_addr
        port = 8000

        # Create socket
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print ("Socket created.")
        # Bind socket
        try:
            soc.bind((host, port))
        except:
            print("Bind failed. Error:\n" + str(sys.exc_info()))
            sys.exit()
        # Have socket listen and queue up to 6 requests
        soc.listen(6)
        print("Socket now listening.")
        # Infinite loop to always accept new connections.
        while True:
            connection, address = soc.accept()
            ip, port = str(address[0]), str(address[1])
            print("Connected at port " + ip + ": " + port)

            try:
                Thread(target=client_thread, args=(connection, ip, port)).start()
                print("\tClient thread started.")
            except:
                print("\tCould not start thread.")
                traceback.print_exc()
        soc.close()

class ClientConnection:
    def __init__(self, connection, ip, port, max_buffer_size):
        self.connection = connection
        self.ip = ip
        self.port = port

# Starts server and waits for connections, creates a thread for each connection
def start_server(ip_addr):
    # Set host and port information
    host = ip_addr
    port = 8000

    # Create socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ("Socket created.")
    # Bind socket
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error:\n" + str(sys.exc_info()))
        sys.exit()
    # Have socket listen and queue up to 6 requests
    soc.listen(6)
    print("Socket now listening.")
    # Infinite loop to always accept new connections.
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected at port " + ip + ": " + port)
        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
            print("\tClient thread started.")
        except:
            print("\tCould not start thread.")
            traceback.print_exc()
    soc.close()

# Thread dispathed for each client while the connection is alive
def client_thread(connection, ip, port, max_buffer_size = BUFFER_SIZE):
    is_active = True
    while is_active:
        # Receive input from the connection
        # client_input = receive_input(connection, max_buffer_size)
        # if "--quit--" in client_input:
        #     print("Client at port " + str(port) + " is requesting to quit.")
        #     connection.close()
        #     print("\tConnection closed.")
        #     is_active = False
        # else:
        #     print("From port " + str(port) + ": " + client_input)
        #     connection.sendall("-".encode("utf8"))

        receive_file(ip, connection, max_buffer_size)

# Receiving a file
def receive_file(target_ip, connection, max_buffer_size):
    # First get file information
    try:
        received = connection.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        # Send acknowledgment
        connection.sendall("^".encode())
    except Exception as error:
        # # Error handling code here
        # print ("Invalid filename or filesize received.\n" + repr(error))
        return None
    # Then start to receive
    try:
        # Progress
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", \
            unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            for _ in progress:
                # Read in incoming data; once over, break
                bytes_read = connection.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                # Write to the file
                f.write(bytes_read)
                # Update progress bar
                progress.update(len(bytes_read))
                connection.sendall("-".encode())
    except Exception as error:
        print ("Something went wrong receiving the file...\n" + repr(error))


# Receiving input
def receive_input(connection, max_buffer_size):
    # Get message and size from connection
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("ERROR: The input size is greater than " + str(client_input_size) + ".")
    # Decode input and process
    decoded_input = client_input.decode("utf8").rstrip()
    result = process_input(decoded_input)
    return result

# Processing input
def process_input(input_str):
    print("Processing input...")
    return ("\"" + input_str + "\"")

# File structure building
def build_file_structure(ip_addr, netfile, base_path):
    # Process netlinks file to get neighbors
    net_lookup = {}
    with open(args.net) as f:
        for line in f.readlines():
            line = line.strip()
            info = line.split(':')
            net_lookup[info[0]] = info[1].split(',')
    neighbors = net_lookup[args.ip]

    # Check if base path exists
    node_folder = "/" + base_path.strip("/")
    if not os.path.exists(node_folder):
        print("Storage path not valid.")
        sys.exit()
    # Check if node folder exists; if not, make it
    # node_folder = base_path + "/" + ip_addr
    # if not os.path.exists(node_folder):
    #     os.makedirs(node_folder)
    # Check if outbox exists; if not, make it
    outbox_path = node_folder + "/outbox"
    if not os.path.exists(outbox_path):
        os.makedirs(outbox_path)
    # Check if inbox exists; if not, make it
    inbox_path = node_folder + "/inbox"
    if not os.path.exists(inbox_path):
        os.makedirs(inbox_path)
    # Check if each neighbor tag exists
    for neighbor in neighbors:
        neighbor_path = inbox_path + "/" + neighbor
        if not os.path.exists(neighbor_path):
            os.makedirs(neighbor_path)

# MAIN
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run client service.')
    parser.add_argument( '--ip', action = 'store', type = str, required = True, \
        help = 'Local IP address.')
    parser.add_argument( '--net', action = 'store', type = str, required = True, \
        help = 'File of network links with each line in the format <LOCAL_IP:NEIGHBOR_IP,NEIGHBOR_IP,etc.>.')
    parser.add_argument( '--path', action = 'store', type = str, required = True, \
        help = 'Path to base directory.')
    args = parser.parse_args()
    build_file_structure(args.ip, args.net, args.path)
    start_server(args.ip)
    