from datetime import datetime

from acarsserver.model.message import Message


class MessageInputMapper:

    @staticmethod
    def map(data, aircraft, client):
        created_at_str = '{} {}'.format(data[4], data[5])

        flight = data[15]
        txt = ' '.join(data[16:])
        created_at = datetime.strptime(created_at_str, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        msg = Message([None, aircraft.id, flight, txt, created_at, client.id], client)

        return msg
