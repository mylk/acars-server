from datetime import datetime

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.model.client import Client


class ClientMapper:

    adapter = None

    def __init__(self):
        self.adapter = SqliteAdapter.get_instance()

    def insert(self, client):
        self.adapter.execute(
            'INSERT INTO clients (ip, last_seen) VALUES (?, ?)',
            (client.ip, client.last_seen)
        )

        self.adapter.connection.commit()
        self.adapter.connection.close()

    def fetch(self, id):
        self.adapter.execute('SELECT id, ip, last_seen FROM clients WHERE id = ?', (id,))
        result = self.adapter.fetchone()
        self.adapter.connection.close()

        client = None
        if result:
            client = Client()
            client.id = result[0]
            client.ip = result[1]
            client.last_seen = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S')

        return client
