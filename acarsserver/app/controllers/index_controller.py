from bottle import template

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.app.controllers.application_controller import ApplicationController
from acarsserver.config import environment
from acarsserver.mapper.db.aircraft import AircraftDbMapper


class IndexController(ApplicationController):
    """Class for handling index page."""

    def index(self):
        """Render index page."""

        root_path = environment.web_root_path

        adapter = SqliteAdapter.get_instance()
        aircrafts = AircraftDbMapper(adapter).fetch_all(('last_seen', 'DESC'), 10)
        adapter.connection.close()

        return template('index.tpl', aircrafts=aircrafts, root_path=root_path)
