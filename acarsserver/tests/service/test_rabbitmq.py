from datetime import datetime
import mock
import pika
import unittest

from acarsserver.model.aircraft import Aircraft
from acarsserver.service.logger import LoggerService
from acarsserver.service.rabbitmq import RabbitMQService


class RabbitMQServiceTestCase(unittest.TestCase):

    logger = None
    rabbitmq = None

    def setUp(self):
        self.logger = LoggerService().get_instance()
        self.rabbitmq = RabbitMQService(self.logger)

    def test_init_sets_channel_and_logger(self):
        self.assertEqual('BlockingChannel', type(self.rabbitmq.channel).__name__)
        self.assertEqual('RootLogger', type(self.logger).__name__)

    def test_publish_enqueues_job(self):
        self.rabbitmq.channel = mock.MagicMock()
        seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        aircraft = Aircraft([None, 'foo', None, seen_datetime, seen_datetime])

        self.rabbitmq.publish(aircraft)

        self.rabbitmq.channel.basic_publish.assert_called_once_with(
            body='{{"id": null, "registration": "foo", "image": null, "first_seen": "{}", "last_seen": "{}"}}'.format(
                seen_datetime,
                seen_datetime
            ),
            exchange='',
            properties=pika.BasicProperties(delivery_mode=2),
            routing_key='image_download'
        )
