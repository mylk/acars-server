#!/usr/bin/python

import os
import socket
import sqlite3
import sys

from acarsserver.model.message import Message

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

        msg = Message.create(data)

        path = '{}/../db/db.sqlite3'.format(os.path.dirname(os.path.realpath(__file__)))
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('INSERT INTO messages (aircraft, flight, received_at) VALUES (?, ?, ?)', (msg.aircraft, msg.flight, msg.received_at))
        conn.commit()
        conn.close()

        print('Message from client {}:{}\n{}\n'.format(address[0], str(address[1]), str(msg)))
    except (KeyboardInterrupt, SystemExit):
        print('Exiting gracefully.')
        break

sock.close()
