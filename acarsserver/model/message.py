from datetime import datetime

from acarsserver.mapper.db.client import ClientDbMapper


class Message:

    id = None
    aircraft = None
    flight = None
    first_seen = None
    last_seen = None
    client = None

    def __init__(self, result, client):
        self.id = result[0]
        self.aircraft = result[1]
        self.flight = result[2]
        self.first_seen = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S')
        self.last_seen = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S')
        self.client = client

    def __str__(self):
        return 'ID: {}, Aircraft: {}, Flight: {}, First Seen:{}, Last Seen:{}, Client ID: {}'.format(
            self.id,
            self.aircraft,
            self.flight,
            self.first_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.last_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.client.id
        )
