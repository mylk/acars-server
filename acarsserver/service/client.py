from datetime import datetime

from acarsserver.model.client import Client


class ClientService:

    @staticmethod
    def map(ip):
        client = Client()
        client.ip = ip
        client.last_seen = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        client.is_online = True if ((datetime.now() - client.last_seen).seconds / 60) <= 30 else False

        return client
