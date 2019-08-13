from acarsserver.app.controllers.assets_controller import AssetsController
from acarsserver.app.controllers.index_controller import IndexController
from acarsserver.config import environment


def setup_routing(app):
    root_path = environment.web_root_path

    # static files
    app.route('{}/img/<path:path>/<filename>'.format(root_path), 'GET', AssetsController.img)
    app.route('{}/css/<filename>'.format(root_path), 'GET', AssetsController.css)
    app.route('{}/js/<filename>'.format(root_path), 'GET', AssetsController.js)

    # home
    app.route('{}/'.format(root_path), 'GET', IndexController().index)
