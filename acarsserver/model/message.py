from datetime import datetime


class Message:

    id = None
    aircraft = None
    flight = None
    first_seen = None
    last_seen = None
    client = None

    def __str__(self):
        return 'ID: {}, Aircraft: {}, Flight: {}, First Seen:{}, Last Seen:{}, Client ID: {}'.format(
            self.id,
            self.aircraft,
            self.flight,
            self.first_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.last_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.client.id
        )
