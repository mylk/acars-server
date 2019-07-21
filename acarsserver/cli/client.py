#!/usr/bin/python

from datetime import datetime
import random
import socket
import sys
import time

HOST = 'localhost';
PORT = 5555;

MESSAGES = [
  '  (null) 3 {} {} 0 -24 H .G-ZBKK  Q0 4 S63A BA0132 ',
  '  (null) 3 {} {} 0 -23 H .F-GRXA  Q0 2 S58A AF123M ',
  '  (null) 3 {} {} 0 -13 H .EI-FHP  Q0 2 S20A DY84PG ',
  '  (null) 3 {} {} 0 -23 H .PK-CMV  16 5 M56A SJJTG3 080346,37000,0842,   3,N 38.980 E 23.424'
]

# create dgram udp socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created.')
except OSError as msg:
    print('Failed to create socket. Error:' + msg)
    sys.exit()

while True:
    now = datetime.now()
    current_date = datetime.strftime(now, '%d/%m/%Y')
    current_time = datetime.strftime(now, '%H:%M:%S')

    msg = random.choice(MESSAGES).format(current_date, current_time)

    try:
        sock.sendto(msg.encode(), (HOST, PORT))

        print('Data sent.')

    except (KeyboardInterrupt, SystemExit):
        print('Exiting gracefully.')
        break
    except OSError as msg:
        print('Error sending data: ' + msg)
        sys.exit()

    time.sleep(5)

sock.close()
