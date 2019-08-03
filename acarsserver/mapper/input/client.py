from datetime import datetime

from acarsserver.model.client import Client


class ClientInputMapper:

    @staticmethod
    def map(ip):
        client = Client()
        client.ip = ip
        client.last_seen = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        client.is_online = True

        return client
