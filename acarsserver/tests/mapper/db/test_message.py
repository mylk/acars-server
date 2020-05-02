from datetime import datetime
import mock
import unittest

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.mapper.db.message import MessageDbMapper
from acarsserver.model.message import Message


class MessageTestCase(unittest.TestCase):
    adapter = None
    mapper = None

    def setUp(self):
        self.adapter = SqliteAdapter.get_instance()
        self.mapper = MessageDbMapper(self.adapter)

    def tearDown(self):
        self.mapper.delete_all()
        self.adapter.connection.close()

    def test_insert_inserts_message_and_returns_row_id(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        aircraft = mock.MagicMock()
        aircraft.id = 1
        client = mock.MagicMock()
        client.id = 1

        message = Message([None, 1, 'foo', 'bar', seen_datetime], client)
        message_id = self.mapper.insert(message, aircraft, client)

        messages = self.mapper.fetch_by('id', message_id)
        self.assertNotEqual([], messages)
        self.assertIsNotNone(message_id)

    def test_fetch_by_returns_none_when_message_does_not_exist(self):
        messages = self.mapper.fetch_by('id', 0)
        self.assertEqual([], messages)

    def test_fetch_by_returns_messages_when_exist(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        aircraft = mock.MagicMock()
        aircraft.id = 1
        client = mock.MagicMock()
        client.id = 1

        message = Message([None, 1, 'foo', 'bar', seen_datetime], client)
        message_id = self.mapper.insert(message, aircraft, client)

        messages = self.mapper.fetch_by('id', message_id)
        self.assertNotEqual([], messages)

    def test_delete_does_nothing_when_message_does_not_exist(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        aircraft = mock.MagicMock()
        aircraft.id = 1
        client = mock.MagicMock()
        client.id = 1

        message = Message([None, 1, 'foo', 'bar', seen_datetime], client)
        message_id = self.mapper.insert(message, aircraft, client)

        message_non_existing = mock.MagicMock()
        message_non_existing.id = 999

        self.mapper.delete(message_non_existing)

        messages = self.mapper.fetch_by('id', message_id)
        self.assertNotEqual([], messages)

    def test_delete_deletes_message_when_exists(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        aircraft = mock.MagicMock()
        aircraft.id = 1
        client = mock.MagicMock()
        client.id = 1

        message = Message([None, 1, 'foo', 'bar', seen_datetime], client)
        message_id = self.mapper.insert(message, aircraft, client)

        messages = self.mapper.fetch_by('id', message_id)
        self.mapper.delete(messages[0])

        messages = self.mapper.fetch_by('id', message_id)
        self.assertEqual([], messages)

    def test_delete_all_deletes_messages_when_exist(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        aircraft = mock.MagicMock()
        aircraft.id = 1
        client = mock.MagicMock()
        client.id = 1

        message = Message([None, 1, 'foo', 'bar', seen_datetime], client)
        message_id = self.mapper.insert(message, aircraft, client)

        self.mapper.delete_all()

        messages = self.mapper.fetch_by('id', message_id)
        self.assertEqual([], messages)
