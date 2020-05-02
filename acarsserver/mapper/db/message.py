from datetime import datetime

from acarsserver.mapper.db.client import ClientDbMapper
from acarsserver.model.message import Message


class MessageDbMapper:

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def insert(self, msg, aircraft, client):
        self.adapter.execute(
            'INSERT INTO messages (aircraft_id, flight, txt, created_at, client_id) VALUES (?, ?, ?, ?, ?)',
            (aircraft.id, msg.flight, msg.txt, msg.created_at, client.id)
        )

        self.adapter.connection.commit()

        return self.adapter.lastrowid

    def fetch_by(self, column, value, order=None, limit=None):
        # default order and limit, if not set
        order = ('id', 'ASC') if order is None else order
        limit = -1 if limit is None else limit

        self.adapter.execute(
            """
                SELECT id, aircraft_id, flight, txt, created_at, client_id
                FROM messages
                WHERE {} = ?
                ORDER BY {} {} LIMIT {}
            """.format(
                column,
                order[0],
                order[1],
                limit
            ),
            (value,)
        )
        results = self.adapter.fetchall()

        # map to models
        messages = []
        for result in results:
            client = ClientDbMapper(self.adapter).fetch(result[5])
            msg = Message(result, client)

            messages.append(msg)

        return messages

    def delete(self, message):
        self.adapter.execute('DELETE FROM messages WHERE id = ?', (message.id,))

        self.adapter.connection.commit()

    def delete_all(self):
        self.adapter.execute('DELETE FROM messages')

        self.adapter.connection.commit()
