import sqlite3
from unittest import TestCase

from acarsserver.adapter.sqlite import SqliteAdapter


class SqliteAdapterTestCase(TestCase):

    def test_get_instance_returns_adapter_cursor(self):
        adapter = SqliteAdapter.get_instance()

        self.assertTrue(isinstance(adapter, sqlite3.Cursor))
