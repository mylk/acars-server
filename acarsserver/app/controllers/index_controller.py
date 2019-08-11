from bottle import template
import os
import sqlite3

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.app.controllers.application_controller import ApplicationController
from acarsserver.config import environment
from acarsserver.mapper.db.message import MessageDbMapper


class IndexController(ApplicationController):
    """Class for handling index page."""

    def index(self):
        """Render index page."""

        root_path = environment.web_root_path

        adapter = SqliteAdapter.get_instance()
        messages = MessageDbMapper(adapter).fetch_all(('last_seen', 'DESC'), 10)
        adapter.connection.close()

        return template('index.tpl', root_path=root_path, messages=messages)
