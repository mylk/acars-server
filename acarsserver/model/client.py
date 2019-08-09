from datetime import datetime


class Client:

    id = None
    ip = None
    last_seen = None
    is_online = None

    def __init__(self, result):
        self.id = result[0]
        self.ip = result[1]
        self.last_seen = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S')
        self.is_online = True if ((datetime.utcnow() - self.last_seen).seconds / 60) <= 30 else False

    def __str__(self):
        return 'ID: {}, IP: {}, Last Seen: {}, Is Online: {}'.format(
            self.id,
            self.ip,
            self.last_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.is_online
        )
