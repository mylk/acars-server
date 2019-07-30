from datetime import datetime


class Client:

    id = None
    ip = None
    last_seen = None

    def __str__(self):
        return 'ID: {}, IP:{}, Last Seen:{}'.format(
            self.id,
            self.ip,
            self.last_seen.strftime('%Y-%m-%d %H:%M:%S')
        )
