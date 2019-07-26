from datetime import datetime

from acarsserver.service.image import Image


class Message:

    aircraft = None
    aircraft_image = None
    flight = None
    received_at = None

    @staticmethod
    def create(data):
        msg = None
        if type(data) == str:
            msg = Message.create_from_string(data)
        elif type(data) == tuple:
            msg = Message.create_from_list(data)
        else:
            return None

        if Image.exists(msg.aircraft):
            print('Aircraft image exists.')
        else:
            msg.aircraft_image = Image.get_aircraft_image(msg.aircraft)
            Image.download_aircraft_image(msg.aircraft_image, msg.aircraft)
            print('Downloaded aircraft image.')

        return msg

    @staticmethod
    def create_from_string(data):
        data = data.decode().split(' ')
        received_at_str = '{} {}'.format(data[4], data[5])

        msg = Message()
        msg.aircraft = data[9][1:]
        msg.flight = data[13]
        msg.received_at = datetime.strptime(received_at_str, '%d/%m/%Y %H:%M:%S')

        return msg

    @staticmethod
    def create_from_list(data):
        msg = Message()
        msg.aircraft = data[0]
        msg.flight = data[1]
        msg.received_at = datetime.strptime(data[2], '%Y-%m-%d %H:%M:%S')

        return msg

    def __str__(self):
        return 'Aircraft: {}, Flight: {}, Received At:{}, Aircraft Image:{}'.format(
            self.aircraft,
            self.flight,
            self.received_at.strftime('%Y-%m-%d %H:%M:%S'),
            self.aircraft_image
        )
