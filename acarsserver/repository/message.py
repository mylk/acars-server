from datetime import datetime

from acarsserver.mapper.db.aircraft import AircraftDbMapper
from acarsserver.mapper.db.client import ClientDbMapper
from acarsserver.model.message import Message


class MessageRepository():

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def fetch_identical(self, msg):
        self.adapter.execute(
            'SELECT id, aircraft_id, flight, first_seen, last_seen, client_id ' +
            'FROM messages ' +
            'WHERE aircraft_id = ? ' +
            'AND flight = ? ' +
            'AND ((strftime("%s", "now", "localtime") - strftime("%s", last_seen, "localtime")) / 60) <= 30',
            (msg.aircraft.id, msg.flight)
        )
        result = self.adapter.fetchone()

        msg = None
        if result:
            aircraft = AircraftDbMapper(self.adapter).fetch(result[1])
            client = ClientDbMapper(self.adapter).fetch(result[5])
            msg = Message(result, aircraft, client)

        return msg

    def update(self, msg, client):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        self.adapter.execute(
            'UPDATE messages SET last_seen = ?, client_id = ? WHERE id = ?',
            (now, client.id, msg.id)
        )
        self.adapter.connection.commit()
