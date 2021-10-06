import unittest

import acarsserver.cli.image_download
from acarsserver.service.logger import LoggerService


class ImageDownloadTestCase(unittest.TestCase):

    image_download = None

    def setUp(self):
        self.image_download = acarsserver.cli.image_download

    def tearDown(self):
        self.image_download.LoggerService = LoggerService

    def test_init_sets_adapter_and_logger(self):
        image_download = self.image_download.ImageDownload()
        self.assertEqual('Cursor', type(image_download.adapter).__name__)
        self.assertEqual('RootLogger', type(image_download.logger).__name__)

    @unittest.skip('Incomplete')
    def test_handle_sets_up_consumer(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_handles_queue_exceptions(self):
        pass

    @unittest.skip('Incomplete')
    def test_callback_asks_image_download(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_handles_queue_ack_exception(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_handles_queue_nack_exception(self):
        pass
