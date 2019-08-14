from datetime import datetime


class Message:

    id = None
    aircraft_id = None
    flight = None
    txt = None
    created_at = None
    client = None

    def __init__(self, result, client):
        self.id = result[0]
        self.aircraft_id = result[1]
        self.flight = result[2]
        self.txt = result[3]
        self.created_at = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S')
        self.client = client

    def __str__(self):
        return 'Aircraft ID: {}, Flight: {}, Created At: {}, Client ID: {}'.format(
            self.aircraft_id,
            self.flight,
            self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            self.client.id
        )
