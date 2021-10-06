#!/usr/bin/python

import json
import socket
import sys

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.config import environment
from acarsserver.mapper.db.aircraft import AircraftDbMapper
from acarsserver.mapper.db.client import ClientDbMapper
from acarsserver.mapper.db.message import MessageDbMapper
from acarsserver.mapper.input.aircraft import AircraftInputMapper
from acarsserver.mapper.input.client import ClientInputMapper
from acarsserver.mapper.input.message import MessageInputMapper
from acarsserver.repository.aircraft import AircraftRepository
from acarsserver.repository.client import ClientRepository
from acarsserver.service.input_decoder import InputDecoderService
from acarsserver.service.input_normalizer import InputNormalizerService
from acarsserver.service.logger import LoggerService
from acarsserver.service.rabbitmq import RabbitMQService


class Listener:

    # all available interfaces
    HOST = ''
    PORT = environment.listener_port
    adapter = None
    logger = None

    def __init__(self):
        self.adapter = SqliteAdapter.get_instance()
        self.logger = LoggerService().get_instance()

    def handle(self):
        # create udp socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.logger.info('Socket created.')
        except OSError as msg:
            self.logger.error('Failed to create socket. Error:' + str(msg))
            sys.exit()

        # bind socket to local host and port
        try:
            sock.bind((self.HOST, self.PORT))
        except OSError as msg:
            self.logger.error('Bind failed. Error: ' + str(msg))
            sys.exit()

        self.logger.info('Socket bind complete.')

        while True:
            try:
                # receive data from client
                request = sock.recvfrom(1024)
                request_dict = json.loads(request[0].decode(), cls=InputDecoderService.get_decoder)
                data = InputNormalizerService.normalize(request_dict)
                address = request[1]
                ip = address[0]
                port = address[1]

                client = ClientInputMapper.map(ip)
                identical = ClientRepository(self.adapter).fetch_identical(client)
                if identical:
                    ClientDbMapper(self.adapter).update(identical)
                    client = identical
                else:
                    ClientDbMapper(self.adapter).insert(client)
                    client = ClientRepository(self.adapter).fetch_identical(client)

                aircraft = AircraftInputMapper.map(data)
                identical = AircraftRepository(self.adapter).fetch_identical(aircraft)
                if identical:
                    identical.last_seen = aircraft.last_seen
                    AircraftDbMapper(self.adapter).update(identical)
                    aircraft = identical
                else:
                    AircraftDbMapper(self.adapter).insert(aircraft)
                    aircraft = AircraftRepository(self.adapter).fetch_identical(aircraft)

                msg = MessageInputMapper.map(data, aircraft, client)
                MessageDbMapper(self.adapter).insert(msg, aircraft, client)

                RabbitMQService(self.logger).publish(aircraft)

                self.logger.info('Message from client {}:{}\n{}'.format(ip, port, str(msg)))
            except (KeyboardInterrupt, SystemExit):
                self.logger.warning('Exiting gracefully.')
                break

        self.adapter.connection.close()

        sock.close()


if __name__ == '__main__':
    Listener().handle()
