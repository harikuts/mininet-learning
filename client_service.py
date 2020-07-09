#!/usr/bin/python
import socket
import sys

"""
This code is based on code from
https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python.
"""

# parser = argparse.ArgumentParser(description='Run as main() to enable data distribution from switch.')
# parser.add_argument( '--div', action = 'store', type = str, required = True, \
#     help = 'IP addresses and divisions.')

def main():
    # Get host and port information
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
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
    main()