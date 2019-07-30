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
        'server = %s\n'
        'host = %s\n'
        'port = %s\n'
        'db_url = %s\n'
        'db_echo = %s\n'
        'reloader = %s\n'
        'debug = %s\n',
        environment.server,
        settings.web_host,
        settings.web_port,
        environment.db_url,
        environment.db_echo,
        environment.reloader,
        environment.debug
    )

    acarsserver = AcarsServer(
        server=environment.server,
        host=settings.web_host,
        port=settings.web_port,
        db_url=environment.db_url,
        db_echo=environment.db_echo,
        reloader=environment.reloader,
        debug=environment.debug
    )

    bottle.run(
        acarsserver.app,
        server=acarsserver.server_type,
        reloader=acarsserver.reloader,
        host=acarsserver.host,
        port=acarsserver.port
    )


if __name__ == '__main__':
    main()
