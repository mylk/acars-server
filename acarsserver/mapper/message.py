from datetime import datetime

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.model.message import Message
from acarsserver.service.image import ImageService


class MessageMapper:

    adapter = None

    def __init__(self):
        self.adapter = SqliteAdapter.get_instance()

    def insert(self, msg):
        self.adapter.execute(
            'INSERT INTO messages (aircraft, flight, first_seen, last_seen) VALUES (?, ?, ?, ?)',
            (msg.aircraft, msg.flight, msg.first_seen, msg.last_seen)
        )
        self.adapter.connection.commit()
        self.adapter.connection.close()

    def fetch_all(self, order=None, limit=None):
        # default order and limit, if not set
        order = ('id', 'ASC') if order is None else order
        limit = -1 if limit is None else limit

        # the actual query
        self.adapter.execute(
            'SELECT id, aircraft, flight, first_seen, last_seen FROM messages ORDER BY {} {} LIMIT {}'.format(
                order[0],
                order[1],
                limit
            )
        )
        results = self.adapter.fetchall()

        self.adapter.connection.close()

        # map to models
        messages = []
        for result in results:
            msg = Message()
            msg.id = result[0]
            msg.aircraft = result[1]
            msg.flight = result[2]
            msg.first_seen = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S')
            msg.last_seen = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S')

            # fetch the aircraft image if missing
            if not ImageService.exists(msg.aircraft):
                print('Downloading {} aircraft image.'.format(msg.aircraft))
                msg.aircraft_image = ImageService.get_aircraft_image(msg.aircraft)
                ImageService.download_aircraft_image(msg.aircraft_image, msg.aircraft)
                print('Aircraft image downloaded.')

            messages.append(msg)

        return messages
