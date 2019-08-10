from datetime import datetime

from acarsserver.model.message import Message
from acarsserver.service.image import ImageService


class MessageInputMapper:

    @staticmethod
    def map(data, aircraft, client):
        last_seen_str = '{} {}'.format(data[4], data[5])

        flight = data[15]
        txt = ' '.join(data[16:])
        first_seen = datetime.strptime(last_seen_str, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        last_seen = datetime.strptime(last_seen_str, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        # nones are id, aircraft_id, client_id
        msg = Message([None, None, flight, txt, first_seen, last_seen, None], aircraft, client)

        return msg
