from datetime import datetime
from unittest import TestCase

from acarsserver.mapper.input.aircraft import AircraftInputMapper
from acarsserver.model.aircraft import Aircraft


class AircraftTestCase(TestCase):
    data = {}
    mapper = None

    def setUp(self):
        self.data = {
            'tail': 'foo',
            'timestamp': int(datetime.utcnow().strftime('%s'))
        }
        self.mapper = AircraftInputMapper()

    def test_map_returns_aircraft_when_all_fields_exist(self):
        datetime_expected = datetime.utcfromtimestamp(self.data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

        aircraft_expected = Aircraft([None, self.data['tail'], None, datetime_expected, datetime_expected])
        aircraft_actual = self.mapper.map(self.data)

        self.assertEqual(dict(aircraft_expected), dict(aircraft_actual))
