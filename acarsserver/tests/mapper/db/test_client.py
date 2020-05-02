from datetime import datetime
import unittest

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.mapper.db.client import ClientDbMapper
from acarsserver.model.client import Client


class ClientTestCase(unittest.TestCase):
    adapter = None
    mapper = None

    def setUp(self):
        self.adapter = SqliteAdapter.get_instance()
        self.mapper = ClientDbMapper(self.adapter)

    def tearDown(self):
        self.mapper.delete_all()
        self.adapter.connection.close()

    def test_insert_inserts_client_and_returns_row_id(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client = Client([None, '127.0.0.1', seen_datetime])

        client_id = self.mapper.insert(client)

        client = self.mapper.fetch(client_id)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client_id)

    def test_fetch_returns_none_when_client_does_not_exist(self):
        client = self.mapper.fetch(1)
        self.assertIsNone(client)

    def test_fetch_returns_client_when_exists(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client = Client([None, '127.0.0.1', seen_datetime])

        client_id = self.mapper.insert(client)

        client = self.mapper.fetch(client_id)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client_id)

    def test_update_does_nothing_when_client_does_not_exist(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client_existing = Client([None, '127.0.0.1', seen_datetime])
        client_id = self.mapper.insert(client_existing)
        client_non_existing = Client([0, '127.0.0.2', seen_datetime])

        self.mapper.update(client_non_existing)

        # assert that existing client was not affected
        client = self.mapper.fetch(client_id)
        self.assertEqual('127.0.0.1', client.ip)

    def test_update_updates_client_when_exists(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client = Client([None, '127.0.0.1', seen_datetime])
        client_id = self.mapper.insert(client)

        client = self.mapper.fetch(client_id)
        client.ip = '127.0.0.2'
        self.mapper.update(client)

        # assert that ip column was updated
        client = self.mapper.fetch(client_id)
        self.assertEqual('127.0.0.2', client.ip)

    def test_delete_does_nothing_when_aircraft_does_not_exist(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client_existing = Client([None, '127.0.0.1', seen_datetime])
        client_id = self.mapper.insert(client_existing)
        client_non_existing = Client([0, '127.0.0.1', seen_datetime])

        self.mapper.delete(client_non_existing)

        # assert that existing client was not affected
        client = self.mapper.fetch(client_id)
        self.assertIsNotNone(client)

    def test_delete_deletes_client_when_exists(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client = Client([None, '127.0.0.1', seen_datetime])
        client_id = self.mapper.insert(client)

        client = self.mapper.fetch(client_id)
        self.mapper.delete(client)

        client = self.mapper.fetch(client_id)
        self.assertIsNone(client)

    def test_delete_all_does_nothing_when_no_clients_exist(self):
        self.mapper.delete_all()

    def test_delete_all_deletes_clients_when_exist(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        client = Client([None, '127.0.0.1', seen_datetime])
        client_id = self.mapper.insert(client)

        self.mapper.delete_all()

        client = self.mapper.fetch(client_id)
        self.assertIsNone(client)
