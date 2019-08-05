#!/usr/bin/python

import os
import sys

from acarsserver.config import environment
from acarsserver.config import settings
from acarsserver.service.logger import LoggerService

HOST = environment.listener_host
PORT = environment.listener_port

logger = LoggerService().get_instance()

try:
    logger.info('Starting acarsdec.')
    os.execlp('acarsdec', '-A', '-N', '{}:{}'.format(HOST, PORT), '-o0', '-r', '0', *settings.acars_frequencies)
except OSError as msg:
    logger.error('Failed to start acarsdec. Error:' + msg)
    sys.exit()
except (KeyboardInterrupt, SystemExit):
    logger.warning('Exiting gracefully.')
    sys.exit()
