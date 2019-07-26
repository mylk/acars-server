from bottle import template
import os
import sqlite3

from acarsserver.model.message import Message

from acarsserver.app.controllers.application_controller import (
    ApplicationController
)


class IndexController(ApplicationController):
    """Class for handling index page."""

    def index(self):
        """Render index page."""

        path = '{}/../../db/db.sqlite3'.format(os.path.dirname(os.path.realpath(__file__)))
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('SELECT aircraft, flight, received_at FROM messages ORDER BY received_at DESC LIMIT 10')
        data = c.fetchall()

        messages = []
        for msg in data:
            messages.append(Message.create(msg))

        return template('index.tpl', messages=messages)
