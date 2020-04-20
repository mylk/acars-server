import datetime
from unittest import TestCase

from acarsserver.model.client import Client


class ClientTestCase(TestCase):
    data = {}

    def setUp(self):
        self.data = [1, '127.0.0.1', datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')]

    def test_init_fills_properties(self):
        client = Client(self.data)

        self.assertEqual(self.data[0], client.id)
        self.assertEqual(self.data[1], client.ip)
        self.assertEqual(datetime.datetime.strptime(self.data[2], '%Y-%m-%d %H:%M:%S'), client.last_seen)

    def test_init_sets_is_online_to_false_when_last_seen_is_more_than_threshold(self):
        self.data[2] = (datetime.datetime.utcnow() - datetime.timedelta(minutes=45)).strftime('%Y-%m-%d %H:%M:%S')
        client = Client(self.data)

        self.assertFalse(client.is_online)

    def test_init_sets_is_online_to_true_when_last_seen_is_less_than_threshold(self):
        client = Client(self.data)

        self.assertTrue(client.is_online)

    def test_str_returns_expected_string(self):
        str_expected = 'ID: {}, IP: {}, Last Seen: {}, Is Online: {}'.format(
            self.data[0],
            self.data[1],
            self.data[2],
            True
        )
        client = Client(self.data)

        self.assertEqual(str_expected, str(client))
