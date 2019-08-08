import json
import pika

from acarsserver.config import environment
from acarsserver.config import settings


class RabbitMQService:

    channel = None
    logger = None

    def __init__(self, logger):
        self.logger = logger

        # prepare rabbitmq client
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=environment.queue_host)
        )
        self.channel = connection.channel()
        self.channel.queue_declare(queue=settings.queue_name_image_download, durable=True)

    def __del__(self):
        self.channel = None

    def publish(self, aircraft):
        self.logger.info('Enqueuing the image downloading of the aircraft #{} named "{}"...'
             .format(aircraft.id, aircraft.registration))

        body = json.dumps(dict(aircraft))

        self.channel.basic_publish(
            exchange='',
            routing_key=settings.queue_name_image_download,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )

        self.logger.info('Successfully enqueued!')
