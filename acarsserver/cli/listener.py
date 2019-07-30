#!/usr/bin/python

import socket
import sys

from acarsserver.config import environment
from acarsserver.mapper.message import MessageMapper
from acarsserver.service.message import MessageService

HOST = '' # all available interfaces
PORT = environment.listener_port

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

        msg = MessageService.map(data)

        MessageMapper().insert(msg)

        print('Message from client {}:{}\n{}\n'.format(address[0], str(address[1]), str(msg)))
    except (KeyboardInterrupt, SystemExit):
        print('Exiting gracefully.')
        break

sock.close()
