from datetime import datetime
from unittest import TestCase

from acarsserver.model.aircraft import Aircraft
from acarsserver.model.message import Message


class AircraftTestCase(TestCase):
    data = []
    messages = []

    def setUp(self):
        now = datetime.utcnow()
        self.messages = [Message([None, None, None, None, now.strftime("%Y-%m-%d %H:%M:%S")], None)]
        self.data = [1, 'foo', 'bar', now, now, self.messages]

    def test_init_fills_properties(self):
        aircraft = Aircraft(self.data, self.messages)

        self.assertEqual(self.data[0], aircraft.id)
        self.assertEqual(self.data[1], aircraft.registration)
        self.assertEqual(self.data[2], aircraft.image)
        self.assertEqual(self.data[3], aircraft.first_seen)
        self.assertEqual(self.data[4], aircraft.last_seen)
        self.assertEqual(self.messages, aircraft.messages)

    def test_str_returns_expected_string(self):
        string_expected = 'ID: {}, Registration: {}, Image: {}, First Seen: {}, Last Seen: {}'.format(
            self.data[0],
            self.data[1],
            self.data[2],
            self.data[3].strftime('%Y-%m-%d %H:%M:%S'),
            self.data[4].strftime('%Y-%m-%d %H:%M:%S'),
        )
        aircraft = Aircraft(self.data, self.messages)

        self.assertEqual(string_expected, str(aircraft))

    def test_iter_returns_expected_iterable(self):
        dict_expected = {
            'id': self.data[0],
            'registration': self.data[1],
            'image': self.data[2],
            'first_seen': self.data[3],
            'last_seen': self.data[4]
        }
        aircraft = Aircraft(self.data, self.messages)

        self.assertEqual(dict_expected, dict(aircraft))
