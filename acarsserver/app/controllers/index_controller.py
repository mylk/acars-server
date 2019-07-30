from bottle import template
import os
import sqlite3

from acarsserver.app.controllers.application_controller import ApplicationController
from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.mapper.message import MessageMapper


class IndexController(ApplicationController):
    """Class for handling index page."""

    def index(self):
        """Render index page."""

        adapter = SqliteAdapter.get_instance()
        messages = MessageMapper(adapter).fetch_all(('last_seen', 'DESC'), 10)
        adapter.connection.close()

        return template('index.tpl', messages=messages)
