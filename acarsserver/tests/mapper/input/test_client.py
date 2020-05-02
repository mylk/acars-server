from datetime import datetime
from unittest import TestCase

from acarsserver.mapper.input.client import ClientInputMapper
from acarsserver.model.client import Client


class ClientTestCase(TestCase):
    data = {}
    mapper = None

    def setUp(self):
        self.data = {
            'ip': '127.0.0.1',
        }
        self.mapper = ClientInputMapper()

    def test_map_returns_client_when_all_fields_exist(self):
        datetime_expected = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        client_expected = Client([None, self.data['ip'], datetime_expected])
        client_actual = self.mapper.map(self.data['ip'])

        self.assertEqual(str(client_expected), str(client_actual))
