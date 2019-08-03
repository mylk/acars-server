from datetime import datetime

from acarsserver.model.message import Message
from acarsserver.service.image import ImageService


class MessageInputMapper:

    @staticmethod
    def map(data, client):

        data = data.decode().split(' ')
        last_seen_str = '{} {}'.format(data[4], data[5])

        msg = Message()
        msg.aircraft = data[9][1:]
        msg.flight = data[13]
        msg.first_seen = datetime.strptime(last_seen_str, '%d/%m/%Y %H:%M:%S')
        msg.last_seen = datetime.strptime(last_seen_str, '%d/%m/%Y %H:%M:%S')
        msg.client = client

        return msg
