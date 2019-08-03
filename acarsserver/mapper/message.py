from datetime import datetime

from acarsserver.model.message import Message
from acarsserver.mapper.client import ClientMapper
from acarsserver.service.image import ImageService


class MessageMapper:

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def insert(self, msg, client):
        self.adapter.execute(
            'INSERT INTO messages (aircraft, flight, first_seen, last_seen, client_id) VALUES (?, ?, ?, ?, ?)',
            (msg.aircraft, msg.flight, msg.first_seen, msg.last_seen, client.id)
        )
        self.adapter.connection.commit()

    def fetch_all(self, order=None, limit=None):
        # default order and limit, if not set
        order = ('id', 'ASC') if order is None else order
        limit = -1 if limit is None else limit

        # the actual query
        self.adapter.execute(
            'SELECT id, aircraft, flight, first_seen, last_seen, client_id FROM messages ORDER BY {} {} LIMIT {}'.format(
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
            msg.id = result[0]
            msg.aircraft = result[1]
            msg.flight = result[2]
            msg.first_seen = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S')
            msg.last_seen = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S')
            msg.client = ClientMapper(self.adapter).fetch(result[5])

            messages.append(msg)

        return messages
