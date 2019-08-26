from datetime import datetime

from acarsserver.model.aircraft import Aircraft


class AircraftInputMapper:

    @staticmethod
    def map(data):
        registration = data['tail']
        first_seen = datetime.utcfromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        last_seen = first_seen

        # nones are id, image
        aircraft = Aircraft([None, registration, None, first_seen, last_seen])

        return aircraft
