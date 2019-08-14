from datetime import datetime

from acarsserver.model.aircraft import Aircraft


class AircraftInputMapper:

    @staticmethod
    def map(data):
        last_seen_str = '{} {}'.format(data[4], data[5])

        registration = data[10]
        first_seen = datetime.strptime(last_seen_str, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        last_seen = datetime.strptime(last_seen_str, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        # nones are id, image
        aircraft = Aircraft([None, registration, None, first_seen, last_seen])

        return aircraft
