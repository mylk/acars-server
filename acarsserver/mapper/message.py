from datetime import datetime

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.model.message import Message
from acarsserver.service.image import Image


class MessageMapper:

    adapter = None

    def __init__(self):
        self.adapter = SqliteAdapter.get_instance()

    def insert(self, msg):
        self.adapter.execute(
            'INSERT INTO messages (aircraft, flight, received_at) VALUES (?, ?, ?)',
            (msg.aircraft, msg.flight, msg.received_at)
        )
        self.adapter.connection.commit()
        self.adapter.connection.close()

    def fetch_all(self, order=None, limit=None):
        # default order and limit, if not set
        order = ('id', 'ASC') if order is None else order
        limit = -1 if limit is None else limit

        # the actual query
        self.adapter.execute(
            'SELECT aircraft, flight, received_at FROM messages ORDER BY {} {} LIMIT {}'.format(
                order[0],
                order[1],
                limit
            )
        )
        results = self.adapter.fetchall()

        # map to models
        messages = []
        for result in results:
            msg = Message()
            msg.aircraft = result[0]
            msg.flight = result[1]
            msg.received_at = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S')

            # fetch the aircraft image if missing
            if not Image.exists(msg.aircraft):
                print('Downloading {} aircraft image.'.format(msg.aircraft))
                msg.aircraft_image = Image.get_aircraft_image(msg.aircraft)
                Image.download_aircraft_image(msg.aircraft_image, msg.aircraft)
                print('Aircraft image downloaded.')

            messages.append(msg)

        return messages
