#!/usr/bin/python

import os
import sys

from acarsserver.config import environment

HOST = environment.listener_host
PORT = environment.listener_port

try:
    print('Starting acarsdec.')
    os.execlp('acarsdec', '-A', '-N', '{}:{}'.format(HOST, PORT), '-o0', '-r', '0', '131.550', '131.525', '131.725', '131.850')
except OSError as msg:
    print('Failed to start acarsdec. Error:' + msg)
    sys.exit()
except (KeyboardInterrupt, SystemExit):
    print('Exiting gracefully.')
    sys.exit()
