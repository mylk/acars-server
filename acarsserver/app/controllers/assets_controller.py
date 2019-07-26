from bottle import static_file

from acarsserver.app.controllers.application_controller import (
    ApplicationController
)


class AssetsController(ApplicationController):
    """Class for handling static assets."""

    def img(filename):
        return static_file(filename, root='acarsserver/app/assets/img')

    def css(filename):
        return static_file(filename, root='acarsserver/app/assets/css')
