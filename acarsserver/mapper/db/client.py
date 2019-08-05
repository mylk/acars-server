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
            client = Client(result)

        return client

    def update(self, client):
        now = datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M:%S')

        self.adapter.execute(
            'UPDATE clients SET last_seen = ? WHERE id = ?',
            (now, client.id)
        )

        self.adapter.connection.commit()
