from datetime import datetime
import unittest

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.mapper.db.client import ClientDbMapper
from acarsserver.model.client import Client
from acarsserver.repository.client import ClientRepository


class ClientTestCase(unittest.TestCase):
    adapter = None
    repository = None

    def setUp(self):
        self.adapter = SqliteAdapter.get_instance()
        self.mapper = ClientDbMapper(self.adapter)
        self.repository = ClientRepository(self.adapter)

    def tearDown(self):
        self.mapper.delete_all()
        self.adapter.connection.close()

    def test_fetch_identical_returns_none_when_client_does_not_exist(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client = Client([None, '127.0.0.1', seen_datetime])

        client = self.repository.fetch_identical(client)
        self.assertEqual(None, client)

    def test_fetch_identical_returns_client_when_exists(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client = Client([None, '127.0.0.1', seen_datetime])

        self.mapper.insert(client)

        client = self.repository.fetch_identical(client)
        self.assertNotEqual(None, client)
