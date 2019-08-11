#!/usr/bin/python

import bottle
from logging import info

from acarsserver import AcarsServer
from acarsserver.config import (
    environment,
    settings
)


def main():
    info('ACARS server started.')

    info(
        '\nApplication settings:\n'
        'web_server = %s\n'
        'web_host = %s\n'
        'web_port = %s\n'
        'web_reloader = %s\n'
        'web_debug = %s\n'
        'web_root_path = %s\n'
        'db_url = %s\n'
        'db_echo = %s\n',
        environment.web_server,
        settings.web_host,
        settings.web_port,
        environment.web_reloader,
        environment.web_debug,
        environment.web_root_path,
        environment.db_url,
        environment.db_echo
    )

    acarsserver = AcarsServer(
        environment.web_debug
    )

    bottle.run(
        acarsserver.app,
        server=environment.web_server,
        reloader=environment.web_reloader,
        host=settings.web_host,
        port=settings.web_port
    )


if __name__ == '__main__':
    main()
