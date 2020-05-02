from datetime import datetime
from unittest import TestCase

from acarsserver.model.aircraft import Aircraft
from acarsserver.model.client import Client
from acarsserver.mapper.input.message import MessageInputMapper
from acarsserver.model.message import Message


class MessageTestCase(TestCase):
    aircraft = None
    client = None
    data = {}
    mapper = None

    def setUp(self):
        timestamp = int(datetime.strftime(datetime.utcnow(), '%s'))
        self.aircraft = Aircraft([1, 'tail', None, timestamp, timestamp])
        self.client = Client([1, '127.0.0.1', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])
        self.data = {
            'flight': 'foo',
            'text': 'bar',
            'timestamp': timestamp
        }
        self.mapper = MessageInputMapper()

    def test_map_returns_message_when_all_fields_exist(self):
        datetime_expected = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        message_expected = Message([
            None,
            self.aircraft.id,
            self.data['flight'],
            self.data['text'],
            datetime_expected,
            self.client.id
        ], self.client)
        message_actual = self.mapper.map(self.data, self.aircraft, self.client)

        self.assertEqual(str(message_expected), str(message_actual))
