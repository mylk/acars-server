from datetime import datetime

from acarsserver.model.client import Client


class ClientInputMapper:

    @staticmethod
    def map(ip):
        client = Client([None, ip, datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')])

        return client
