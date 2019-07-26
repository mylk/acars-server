from bottle import template

from acarsserver.app.controllers.application_controller import (
    ApplicationController
)


class IndexController(ApplicationController):
    """Class for handling index page."""

    def index(self):
        """Render index page."""
        return template('index.tpl')
