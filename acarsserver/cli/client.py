#!/usr/bin/python

import os
import sys

from acarsserver.config import environment
from acarsserver.config import settings

HOST = environment.listener_host
PORT = environment.listener_port

try:
    print('Starting acarsdec.')
    os.execlp('acarsdec', '-A', '-N', '{}:{}'.format(HOST, PORT), '-o0', '-r', '0', *settings.acars_frequencies)
except OSError as msg:
    print('Failed to start acarsdec. Error:' + msg)
    sys.exit()
except (KeyboardInterrupt, SystemExit):
    print('Exiting gracefully.')
    sys.exit()
