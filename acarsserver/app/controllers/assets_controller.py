from bottle import static_file

from acarsserver.app.controllers.application_controller import ApplicationController


class AssetsController(ApplicationController):
    """Class for handling static assets."""

    def img(path, filename):
        return static_file(filename, root='acarsserver/app/assets/img/{}'.format(path))

    def css(filename):
        return static_file(filename, root='acarsserver/app/assets/css')

    def js(filename):
        return static_file(filename, root='acarsserver/app/assets/js')
