import os
import sqlite3


class SqliteAdapter:

    @staticmethod
    def get_instance():
        # @TODO use the one defined in config
        path = '{}/../db/db.sqlite3'.format(os.path.dirname(os.path.realpath(__file__)))

        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        return cursor
