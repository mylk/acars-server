#!/usr/bin/python

from datetime import datetime
import random
import socket
import sys
import time

from acarsserver.config import environment
from acarsserver.service.logger import LoggerService


class ClientFake:

    HOST = environment.listener_host
    PORT = environment.listener_port
    MESSAGES = [
        '  client 3 {} {} 0 -25 2  VP-BOA  Q0 0 S98A FV5786 ',
        '  client 3 {} {} 0 -24 H  VP-BOA  Q0 1 S99A FV5786 ',
        '  client 3 {} {} 0 -24 H  VP-BOA  16 2 M87A FV5786 143218,36000,1807, 267,N 38.027 E 24.548',
        '  client 3 {} {} 1 -25 H  VP-BOA  SA 3 S01A FV5786 0EV143628V/',
        '  client 3 {} {} 0 -26 H  EC-MIH K _d 1 S21A UX1302 ',
        '  client 3 {} {} 0 -25 H  EC-MIH  83 4 M22A UX1302 LLBG,LEMD,071445, 37.14,  23.05,40000,256,- 70.9, 20200',
        '  client 3 {} {} 0 -25 X  CEPL21  B9 1 L03A XA0001 /LTAI.TI2/024LTAIA5853',
        '  client 3 {} {} 0 -23 X  CEPL21  B9 1 L03A XA0001 /LTAI.TI2/024LTAIA5853',
        '  client 3 {} {} 0 -19 H   OKVEA \x15 H1 9 104P GS0943 #T1B CLIMB 1 B\r\n48044824062.0064.8079081051053084.8080.310310204.403.630730900\r\n094.9094.9090.0090.200000000.800.8000000001100110110404950950\r\n'
    ]
    logger = None

    def __init__(self):
        self.logger = LoggerService().get_instance()

    def handle(self):
        # create dgram udp socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.logger.info('Socket created.')
        except OSError as msg:
            self.logger.error('Failed to create socket. Error:' + str(msg))
            sys.exit()

        while True:
            now = datetime.utcnow()
            current_date = datetime.strftime(now, '%d/%m/%Y')
            current_time = datetime.strftime(now, '%H:%M:%S')

            msg = random.choice(self.MESSAGES).format(current_date, current_time)

            try:
                sock.sendto(msg.encode(), (self.HOST, self.PORT))
                self.logger.info('Data sent.')
            except (KeyboardInterrupt, SystemExit):
                self.logger.warning('Exiting gracefully.')
                break
            except OSError as msg:
                self.logger.error('Error sending data: ' + str(msg))
                sys.exit()

            time.sleep(5)

        sock.close()


if __name__ == '__main__':
    ClientFake().handle()
