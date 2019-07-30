from datetime import datetime

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.model.client import Client


class ClientRepository():

    adapter = None

    def __init__(self):
        self.adapter = SqliteAdapter.get_instance()

    def fetch_identical(self, client):
        self.adapter.execute('SELECT id, ip, last_seen FROM clients WHERE ip = ?', (client.ip,))
        result = self.adapter.fetchone()
        self.adapter.connection.close()

        client = None
        if result:
            client = Client()
            client.id = result[0]
            client.ip = result[1]
            client.last_seen = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S')

        return client

    def update(self, client):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        self.adapter.execute(
            'UPDATE clients SET last_seen = ? WHERE id = ?',
            (now, client.id)
        )

        self.adapter.connection.commit()
        self.adapter.connection.close()
