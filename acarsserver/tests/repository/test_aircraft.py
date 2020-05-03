from datetime import datetime
import unittest

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.mapper.db.aircraft import AircraftDbMapper
from acarsserver.model.aircraft import Aircraft
from acarsserver.repository.aircraft import AircraftRepository


class AircraftTestCase(unittest.TestCase):
    adapter = None
    repository = None

    def setUp(self):
        self.adapter = SqliteAdapter.get_instance()
        self.mapper = AircraftDbMapper(self.adapter)
        self.repository = AircraftRepository(self.adapter)

    def tearDown(self):
        self.mapper.delete_all()
        self.adapter.connection.close()

    def test_fetch_identical_returns_none_when_aircraft_does_not_exist(self):
        seen_datetime = datetime.utcnow()
        aircraft = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])

        aircraft = self.repository.fetch_identical(aircraft)
        self.assertEqual(None, aircraft)

    def test_fetch_identical_returns_aircraft_when_exists(self):
        seen_datetime = datetime.utcnow()
        aircraft = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])

        self.mapper.insert(aircraft)

        aircraft = self.repository.fetch_identical(aircraft)
        self.assertNotEqual(None, aircraft)
