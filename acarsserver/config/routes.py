from acarsserver.app.controllers.assets_controller import AssetsController
from acarsserver.app.controllers.index_controller import IndexController


def setup_routing(app):
    # static files
    app.route('/img/<path>/<filename>', 'GET', AssetsController.img)
    app.route('/css/<filename>', 'GET', AssetsController.css)
    app.route('/js/<filename>', 'GET', AssetsController.js)

    # home
    app.route('/', 'GET', IndexController().index)
