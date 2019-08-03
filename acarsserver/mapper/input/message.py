from datetime import datetime

from acarsserver.model.message import Message
from acarsserver.service.image import ImageService


class MessageInputMapper:

    @staticmethod
    def map(data, client):

        data = data.decode().split(' ')
        last_seen_str = '{} {}'.format(data[4], data[5])

        aircraft = data[9][1:]
        flight = data[13]
        first_seen = datetime.strptime(last_seen_str, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        last_seen = datetime.strptime(last_seen_str, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        msg = Message([None, aircraft, flight, first_seen, last_seen], client)

        return msg
