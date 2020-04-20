from datetime import datetime
from unittest import TestCase

from acarsserver.model.client import Client
from acarsserver.model.message import Message


class MessageTestCase(TestCase):
    client = None
    data = {}

    def setUp(self):
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.client = Client([1, '127.0.0.1', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])
        self.data = [1, 2, 'foo', 'bar', timestamp]

    def test_init_fills_properties(self):
        message = Message(self.data, self.client)

        self.assertEqual(self.data[0], message.id)
        self.assertEqual(self.data[1], message.aircraft_id)
        self.assertEqual(self.data[2], message.flight)
        self.assertEqual(self.data[3], message.txt)
        self.assertEqual(datetime.strptime(self.data[4], '%Y-%m-%d %H:%M:%S'), message.created_at)
        self.assertEqual(self.client, message.client)

    def test_str_returns_expected_string(self):
        str_expected = 'Aircraft ID: {}, Flight: {}, Created At: {}, Client ID: {}'.format(
            self.data[1],
            self.data[2],
            self.data[4],
            self.client.id
        )
        message = Message(self.data, self.client)

        self.assertEqual(str_expected, str(message))
