from datetime import datetime
from webtest import TestApp
import unittest

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.mapper.db.aircraft import AircraftDbMapper
from acarsserver.mapper.db.client import ClientDbMapper
from acarsserver.mapper.db.message import MessageDbMapper
from acarsserver.model.aircraft import Aircraft
from acarsserver.model.client import Client
from acarsserver.model.message import Message
from acarsserver.tests.app.controllers import helper


class IndexControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.adapter = SqliteAdapter.get_instance()
        self.aircraftDbMapper = AircraftDbMapper(self.adapter)
        self.clientDbMapper = ClientDbMapper(self.adapter)
        self.messageDbMapper = MessageDbMapper(self.adapter)

    def tearDown(self):
        self.aircraftDbMapper.delete_all()
        self.clientDbMapper.delete_all()
        self.messageDbMapper.delete_all()
        self.adapter.connection.close()

    def test_index(self):
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        aircraft = Aircraft([None, 'AIRCRAFT-1', None, seen_datetime, seen_datetime])
        aircraft_id = self.aircraftDbMapper.insert(aircraft)
        aircraft = self.aircraftDbMapper.fetch(aircraft_id)

        client = Client([None, '127.0.0.1', seen_datetime])
        client_id = self.clientDbMapper.insert(client)
        client = self.clientDbMapper.fetch(client_id)

        message = Message([None, 1, 'FLIGHT-1', 'THE MESSAGE', seen_datetime], client)
        self.messageDbMapper.insert(message, aircraft, client)

        app = TestApp(helper.get_app())
        response = app.get('/')

        self.assertIn(b'AIRCRAFT-1', response.body)
        self.assertIn(b'FLIGHT-1', response.body)
        self.assertIn(b'THE MESSAGE', response.body)
        self.assertEqual('200 OK', response.status)
