from bottle import template
import os
import sqlite3

from acarsserver.app.controllers.application_controller import ApplicationController
from acarsserver.mapper.message import MessageMapper


class IndexController(ApplicationController):
    """Class for handling index page."""

    def index(self):
        """Render index page."""

        messages = MessageMapper().fetch_all(('last_seen', 'DESC'), 10)

        return template('index.tpl', messages=messages)
