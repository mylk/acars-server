#!/usr/bin/python

import os
import sys

from acarsserver.config import environment
from acarsserver.config import settings
from acarsserver.service.logger import LoggerService


class Client:

    HOST = environment.listener_host
    PORT = environment.listener_port
    logger = None

    def __init__(self):
        self.logger = LoggerService().get_instance()

    def handle(self):
        try:
            self.logger.info('Starting acarsdec.')
            os.execlp('acarsdec', '-A', '-N', '{}:{}'.format(self.HOST, self.PORT), '-o0', '-r', '0', *settings.acars_frequencies)
        except OSError as msg:
            self.logger.error('Failed to start acarsdec. Error:' + str(msg))
            sys.exit()
        except (KeyboardInterrupt, SystemExit):
            self.logger.warning('Exiting gracefully.')
            sys.exit()


if __name__ == '__main__':
    Client().handle()
