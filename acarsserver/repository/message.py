from datetime import datetime

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.mapper.client import ClientMapper
from acarsserver.model.message import Message


class MessageRepository():

    adapter = None

    def __init__(self):
        self.adapter = SqliteAdapter.get_instance()

    def fetch_identical(self, msg):
        self.adapter.execute(
            'SELECT id, aircraft, flight, first_seen, last_seen, client_id ' +
            'FROM messages ' +
            'WHERE aircraft = ? ' +
            'AND flight = ? ' +
            'AND ((strftime("%s", "now", "localtime") - strftime("%s", last_seen)) / 60) <= 30',
            (msg.aircraft, msg.flight)
        )
        result = self.adapter.fetchone()

        self.adapter.connection.close()

        msg = None
        if result:
            # @TODO: duplicate code
            msg = Message()
            msg.id = result[0]
            msg.aircraft = result[1]
            msg.flight = result[2]
            msg.first_seen = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S')
            msg.last_seen = datetime.strptime(result[4], '%Y-%m-%d %H:%M:%S')
            msg.client = ClientMapper().fetch(result[5])

        return msg

    def update(self, msg, client):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        self.adapter.execute(
            'UPDATE messages SET last_seen = ?, client_id = ? WHERE id = ?',
            (now, client.id, msg.id)
        )
        self.adapter.connection.commit()
        self.adapter.connection.close()
