import bottle

from acarsserver.config import routes

__version__ = '0.2.0'


class AcarsServer:

    template_path = './acarsserver/app/views/'

    def __init__(self, server, host, port, db_url, db_echo, reloader, debug):
        self.server_type = server
        self.host = host
        self.port = port
        self.reloader = reloader
        self.debug = debug

        self.app = bottle.Bottle()

        routes.setup_routing(self.app)

        if self.template_path not in bottle.TEMPLATE_PATH:
            bottle.TEMPLATE_PATH.append(self.template_path)
        if './' in bottle.TEMPLATE_PATH:
            bottle.TEMPLATE_PATH.remove('./')
        if './views' in bottle.TEMPLATE_PATH:
            bottle.TEMPLATE_PATH.remove('./views')

        bottle.debug(self.debug)
