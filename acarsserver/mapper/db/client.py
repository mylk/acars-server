from datetime import datetime

from acarsserver.model.client import Client


class ClientDbMapper:

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def insert(self, client):
        self.adapter.execute(
            'INSERT INTO clients (ip, last_seen) VALUES (?, ?)',
            (client.ip, client.last_seen)
        )

        self.adapter.connection.commit()

    def fetch(self, id):
        self.adapter.execute('SELECT id, ip, last_seen FROM clients WHERE id = ?', (id,))
        result = self.adapter.fetchone()

        client = None
        if result:
            client = Client()
            client.id = result[0]
            client.ip = result[1]
            client.last_seen = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S')
            client.is_online = True if ((datetime.now() - client.last_seen).seconds / 60) <= 30 else False

        return client
