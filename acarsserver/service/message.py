from datetime import datetime

from acarsserver.model.message import Message
from acarsserver.service.image import ImageService


class MessageService:

    @staticmethod
    def map(data):

        data = data.decode().split(' ')
        received_at_str = '{} {}'.format(data[4], data[5])

        msg = Message()
        msg.aircraft = data[9][1:]
        msg.flight = data[13]
        msg.received_at = datetime.strptime(received_at_str, '%d/%m/%Y %H:%M:%S')

        if not ImageService.exists(msg.aircraft):
            print('Downloading {} aircraft image.'.format(msg.aircraft))
            msg.aircraft_image = ImageService.get_aircraft_image(msg.aircraft)
            ImageService.download_aircraft_image(msg.aircraft_image, msg.aircraft)
            print('Aircraft image downloaded.')

        return msg
