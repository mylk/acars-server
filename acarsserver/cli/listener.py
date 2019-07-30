#!/usr/bin/python

import socket
import sys

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.config import environment
from acarsserver.mapper.client import ClientMapper
from acarsserver.mapper.message import MessageMapper
from acarsserver.repository.client import ClientRepository
from acarsserver.repository.message import MessageRepository
from acarsserver.service.client import ClientService
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

adapter = SqliteAdapter.get_instance()

while True:
    try:
        # receive data from client
        request = sock.recvfrom(1024)
        data = request[0]
        ip = request[1][0]
        port = request[1][1]

        client = ClientService.map(ip)
        identical = ClientRepository(adapter).fetch_identical(client)
        if identical:
            # @TODO move to mapper?
            ClientRepository(adapter).update(identical)
            client = identical
        else:
            ClientMapper(adapter).insert(client)
            client = ClientRepository(adapter).fetch_identical(client)

        msg = MessageService.map(data)
        identical = MessageRepository(adapter).fetch_identical(msg)
        if identical:
            # @TODO move to mapper?
            MessageRepository(adapter).update(identical, client)
            msg = identical
        else:
            MessageMapper(adapter).insert(msg, client)
            msg = MessageRepository(adapter).fetch_identical(msg)

        print('Message from client {}:{}\n{}\n'.format(ip, port, str(msg)))
    except (KeyboardInterrupt, SystemExit):
        print('Exiting gracefully.')
        break

adapter.connection.close()

sock.close()
