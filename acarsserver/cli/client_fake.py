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
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-25,"error":0,"mode":"2","label":"Q0","block_id":"0","ack":false,"tail":"VP-BOA","flight":"FV5786","msgno":"S98A"}}',
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-24,"error":0,"mode":"2","label":"Q0","block_id":"1","ack":false,"tail":"VP-BOA","flight":"FV5786","msgno":"S99A"}}',
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-25,"error":0,"mode":"H","label":"16","block_id":"2","ack":false,"tail":"VP-BOA","flight":"FV5786","msgno":"M87A","text":"143218,36000,1807, 267,N 38.027 E 24.548"}}',
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-25,"error":0,"mode":"H","label":"SA","block_id":"3","ack":false,"tail":"VP-BOA","flight":"FV5786","msgno":"S01A","text":"0EV143628V/"}}',
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-26,"error":0,"mode":"H","label":"_d","block_id":"1","ack":false,"tail":"EC-MIH","flight":"UX1302","msgno":"S21A"}}',
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-25,"error":0,"mode":"H","label":"83","block_id":"4","ack":false,"tail":"EC-MIH","flight":"UX1302","msgno":"M22A","text":"LLBG,LEMD,071445, 37.14,  23.05,40000,256,- 70.9, 20200"}}',
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-25,"error":0,"mode":"X","label":"B9","block_id":"1","ack":false,"tail":"CEPL21","flight":"XA0001","msgno":"L03A","text":"/LTAI.TI2/024LTAIA5853"}}',
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-23,"error":0,"mode":"X","label":"B9","block_id":"1","ack":false,"tail":"CEPL21","flight":"XA0001","msgno":"L03A","text":"/LTAI.TI2/024LTAIA5853"}}',
        '{{"timestamp":{},"station_id":"client","channel":2,"freq":131.725,"level":-19,"error":0,"mode":"H","label":"H1","block_id":"9","ack":false,"tail":"OKVEA","flight":"GS0943","msgno":"104P","text":"#T1B CLIMB 1 B\r\n48044824062.0064.8079081051053084.8080.310310204.403.630730900\r\n094.9094.9090.0090.200000000.800.8000000001100110110404950950\r\n"}}'
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
            current_timestamp = datetime.strftime(datetime.utcnow(), '%s')
            msg = random.choice(self.MESSAGES).format(current_timestamp)

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
