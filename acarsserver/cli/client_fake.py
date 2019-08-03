#!/usr/bin/python

from datetime import datetime
import random
import socket
import sys
import time

from acarsserver.config import environment

HOST = environment.listener_host
PORT = environment.listener_port

MESSAGES = [
    '  (null) 3 {} {} 0 -24 H .G-ZBKK  Q0 4 S63A BA0132 ',
    '  (null) 3 {} {} 0 -23 H .PK-CMV  16 5 M56A SJJTG3 080346,37000,0842,   3,N 38.980 E 23.424',
    '  (null) 3 {} {} 0 -18 H .A6-BLM \x15 H1 1 D15A EY063G #DFB<407>GEG  29 \r\n A6-BLMETD44X    PO  720108190142080000000021672BCG4BACMFGE24\r\nPO 111 123\r\nPO 110 122\r\nPO 110 116\r\nPO 11) 11)\r\nES 140 140\r\nTA 133 126\r\nTA 145 125\r\nIC 142 127\r\nDC 109 114\r\nPOEMP 557  44  0   0',
    '  (null) 3 {} {} 0 -22 2 .OO-SNF \x15 Q0 4 S55A SN089E ',
    '  (null) 3 {} {} 0 -24 H .G-LCYM A _d 6 M10A CJ2220 ',
    '  (null) 3 {} {} 2 -25 H .G-LCYM  H1 9 C08B CJ2220 #CFB82203  142629\n14383213 8551735\n14482114 935 664\n',
    '  (null) 3 {} {} 0 -22 H .G-LCYM  H1 3 C09D CJ2220 #CFB4393102195   0   0\n14393202218   0   0\n14393212249   0   0\n14395912195   0   0\n14400302195   0   0\n14410103249   0   0\n14420513384   0   0\n14421403384   0   0\n14544515310   0   0\n14551105310   0   0\n',
    '  (null) 3 {} {} 0 -24 H .PH-BFH  H1 8 D95A KL0174 #DFB(POS-KLM174D -3719N02455E/150203 F400\r\nRMK/FUEL  29.8 M0.88)',
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
