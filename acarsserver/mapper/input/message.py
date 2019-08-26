from datetime import datetime

from acarsserver.model.message import Message


class MessageInputMapper:

    @staticmethod
    def map(data, aircraft, client):
        flight = data['flight']
        txt = data['text']
        created_at = datetime.utcfromtimestamp(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

        msg = Message([None, aircraft.id, flight, txt, created_at, client.id], client)

        return msg
