from acarsserver.app.controllers.assets_controller import AssetsController
from acarsserver.app.controllers.index_controller import IndexController


def setup_routing(app):
    # static files
    app.route('/img/<filename>', 'GET', AssetsController.img)
    app.route('/css/<filename>', 'GET', AssetsController.css)

    # home
    app.route('/', 'GET', IndexController().index)
