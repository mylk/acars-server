import json
import pika
from pika.exceptions import AMQPChannelError, AMQPConnectionError, ChannelClosed, \
ConnectionClosed, DuplicateConsumerTag, NoFreeChannels

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.config import environment
from acarsserver.config import settings
from acarsserver.model.aircraft import Aircraft
from acarsserver.service.image import ImageService
from acarsserver.service.logger import LoggerService


class ImageDownload:

    adapter = None
    logger = None

    def __init__(self):
        self.adapter = SqliteAdapter.get_instance()
        self.logger = LoggerService().get_instance()

    def handle(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=environment.queue_host)
            )

            channel = connection.channel()
            channel.queue_declare(queue=settings.queue_name_image_download, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=settings.queue_name_image_download, on_message_callback=self.callback)

            channel.start_consuming()
        except (
                AMQPConnectionError, AMQPChannelError, ChannelClosed,
                ConnectionClosed, DuplicateConsumerTag, NoFreeChannels
        ) as ex_consume:
            self.logger.error(str(ex_consume))
            return None

        self.logger.info('RabbitMQ connection has been set up.')

    def callback(self, channel, method, properties, body):
        try:
            body_dict = json.loads(body)
            aircraft = Aircraft([body_dict['id'], body_dict['registration'], body_dict['image']])

            ImageService(self.adapter, self.logger).handle(aircraft)

            channel.basic_ack(delivery_tag=method.delivery_tag)

            self.logger.info('RabbitMQ job done!')
        except (
                AMQPConnectionError, AMQPChannelError, ChannelClosed,
                ConnectionClosed, NoFreeChannels
        ) as ex_ack:
            self.logger.error(str(ex_ack))

            try:
                channel.basic_nack(delivery_tag=method.delivery_tag)
                return None
            except (
                    AMQPConnectionError, AMQPChannelError, ChannelClosed,
                    ConnectionClosed, NoFreeChannels
            ) as ex_nack:
                self.logger.error(str(ex_nack))
                return None


if __name__ == '__main__':
    ImageDownload().handle()
