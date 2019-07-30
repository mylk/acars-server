import bottle

from acarsserver.config import routes

__version__ = '0.2.0'


class AcarsServer:

    def __init__(
        self,
        server='auto',
        host='0.0.0.0',
        port=8080,
        db_url='sqlite:///:memory:',
        db_echo=False,
        reloader=False,
        debug=False,
        template_path='./acarsserver/app/views/'
    ):
        self.server_type = server
        self.host = host
        self.port = port
        self.reloader = reloader
        self.debug = debug

        self.app = bottle.Bottle()

        routes.setup_routing(self.app)

        if template_path not in bottle.TEMPLATE_PATH:
            bottle.TEMPLATE_PATH.append(template_path)
        if './' in bottle.TEMPLATE_PATH:
            bottle.TEMPLATE_PATH.remove('./')
        if './views' in bottle.TEMPLATE_PATH:
            bottle.TEMPLATE_PATH.remove('./views')

        bottle.debug(self.debug)
