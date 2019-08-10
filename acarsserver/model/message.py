from datetime import datetime


class Message:

    id = None
    aircraft = None
    flight = None
    txt = None
    first_seen = None
    last_seen = None
    client = None

    def __init__(self, result, aircraft, client):
        self.id = result[0]
        self.aircraft = aircraft
        self.flight = result[2]
        self.txt = result[3]
        self.first_seen = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S')
        self.last_seen = datetime.strptime(result[5], '%Y-%m-%d %H:%M:%S')
        self.client = client

    def __str__(self):
        return 'ID: {}, Aircraft ID: {}, Flight: {}, First Seen: {}, Last Seen: {}, Client ID: {}'.format(
            self.id,
            self.aircraft.id,
            self.flight,
            self.first_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.last_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.client.id
        )
