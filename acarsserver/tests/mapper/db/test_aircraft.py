from datetime import datetime
import unittest

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.mapper.db.aircraft import AircraftDbMapper
from acarsserver.model.aircraft import Aircraft


class AircraftTestCase(unittest.TestCase):
    adapter = None
    mapper = None

    def setUp(self):
        self.adapter = SqliteAdapter.get_instance()
        self.mapper = AircraftDbMapper(self.adapter)

    def tearDown(self):
        self.mapper.delete_all()
        self.adapter.connection.close()

    def test_insert_inserts_aircraft_and_returns_row_id(self):
        seen_datetime = datetime.utcnow()
        aircraft = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])

        aircraft_id = self.mapper.insert(aircraft)

        aircrafts = self.mapper.fetch_all()
        self.assertEqual(1, len(aircrafts))
        self.assertIsNotNone(aircraft_id)

    def test_fetch_returns_none_when_aircraft_does_not_exist(self):
        aircraft = self.mapper.fetch(1)
        self.assertIsNone(aircraft)

    def test_fetch_returns_aircraft_when_exists(self):
        seen_datetime = datetime.utcnow()
        aircraft = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])

        aircraft_id = self.mapper.insert(aircraft)

        aircraft = self.mapper.fetch(aircraft_id)
        self.assertIsNotNone(aircraft)

    def test_fetch_all_returns_empty_array_when_no_aircrafts_exist(self):
        aircrafts = self.mapper.fetch_all()
        self.assertEqual([], aircrafts)

    def test_fetch_all_returns_all_aircrafts_when_exist(self):
        seen_datetime = datetime.utcnow()
        self.mapper.insert(Aircraft([None, 'foo', None, seen_datetime, seen_datetime]))
        self.mapper.insert(Aircraft([None, 'bar', None, seen_datetime, seen_datetime]))

        aircrafts = self.mapper.fetch_all()
        self.assertEqual(2, len(aircrafts))

    def test_update_does_nothing_when_aircraft_does_not_exist(self):
        seen_datetime = datetime.utcnow()
        aircraft_existing = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])
        aircraft_id = self.mapper.insert(aircraft_existing)
        aircraft_non_existing = Aircraft([0, 'foo', 'bar', seen_datetime, seen_datetime])

        self.mapper.update(aircraft_non_existing)

        # assert that existing aircraft was not affected
        aircraft = self.mapper.fetch(aircraft_id)
        self.assertIsNone(aircraft.image)

    def test_update_updates_aircraft_when_exists(self):
        seen_datetime = datetime.utcnow()
        aircraft = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])
        aircraft_id = self.mapper.insert(aircraft)

        aircraft = self.mapper.fetch(aircraft_id)
        aircraft.image = 'bar'
        self.mapper.update(aircraft)

        # assert that image column was updated
        aircraft = self.mapper.fetch(aircraft_id)
        self.assertEqual('bar', aircraft.image)

    def test_delete_does_nothing_when_aircraft_does_not_exist(self):
        seen_datetime = datetime.utcnow()
        aircraft_existing = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])
        aircraft_id = self.mapper.insert(aircraft_existing)
        aircraft_non_existing = Aircraft([0, 'foo', 'bar', seen_datetime, seen_datetime])

        self.mapper.delete(aircraft_non_existing)

        # assert that existing aircraft was not affected
        aircraft = self.mapper.fetch(aircraft_id)
        self.assertIsNotNone(aircraft)

    def test_delete_deletes_aircraft_when_exists(self):
        seen_datetime = datetime.utcnow()
        aircraft = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])
        aircraft_id = self.mapper.insert(aircraft)

        aircraft = self.mapper.fetch(aircraft_id)
        self.mapper.delete(aircraft)

        aircraft = self.mapper.fetch(aircraft_id)
        self.assertIsNone(aircraft)

    def test_delete_all_does_nothing_when_no_aircrafts_exist(self):
        self.mapper.delete_all()

    def test_delete_all_deletes_aircrafts_when_exist(self):
        seen_datetime = datetime.utcnow()
        aircraft = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])
        aircraft_id = self.mapper.insert(aircraft)

        self.mapper.delete_all()

        aircraft = self.mapper.fetch(aircraft_id)
        self.assertIsNone(aircraft)
