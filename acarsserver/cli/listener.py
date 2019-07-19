#! /usr/bin/python

import socket
import sys

HOST = '' # all available interfaces
PORT = 5555

# create udp socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created.')
except OSError as msg:
    print('Failed to create socket. Error:' + msg)
    sys.exit()

# bind socket to local host and port
try:
    sock.bind((HOST, PORT))
except OSError as msg:
    print('Bind failed. Error: ' + msg)
    sys.exit()

print('Socket bind complete.')

while True:
    try:
        # receive data from client
        request = sock.recvfrom(1024)
        data = request[0]
        address = request[1]

        print('Message from client {}:{}\n{}'.format(address[0], str(address[1]), data.decode('utf-8')))
    except (KeyboardInterrupt, SystemExit):
        print('Exiting gracefully.')
        break

sock.close()
