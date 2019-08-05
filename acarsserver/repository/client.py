from datetime import datetime

from acarsserver.model.client import Client


class ClientRepository():

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def fetch_identical(self, client):
        self.adapter.execute('SELECT id, ip, last_seen FROM clients WHERE ip = ?', (client.ip,))
        result = self.adapter.fetchone()

        client = None
        if result:
            client = Client(result)

        return client
