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

        return self.adapter.lastrowid

    def fetch(self, client_id):
        self.adapter.execute('SELECT id, ip, last_seen FROM clients WHERE id = ?', (client_id,))
        result = self.adapter.fetchone()

        client = None
        if result:
            client = Client(result)

        return client

    def update(self, client):
        now = datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M:%S')

        self.adapter.execute(
            'UPDATE clients SET ip = ?, last_seen = ? WHERE id = ?',
            (client.ip, now, client.id)
        )

        self.adapter.connection.commit()

    def delete(self, client):
        self.adapter.execute('DELETE FROM clients WHERE id = ?', (client.id,))

        self.adapter.connection.commit()

    def delete_all(self):
        self.adapter.execute('DELETE FROM clients')

        self.adapter.connection.commit()
