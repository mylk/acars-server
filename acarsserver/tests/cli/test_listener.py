import unittest

import acarsserver.cli.listener
from acarsserver.service.logger import LoggerService


class ListenerTestCase(unittest.TestCase):

    listener = None

    def setUp(self):
        self.listener = acarsserver.cli.listener

    def tearDown(self):
        self.listener.LoggerService = LoggerService

    def test_init_sets_adapter_and_logger(self):
        image_download = self.listener.Listener()
        self.assertEqual('Cursor', type(image_download.adapter).__name__)
        self.assertEqual('RootLogger', type(image_download.logger).__name__)

    @unittest.skip('Incomplete')
    def test_handle_handles_exceptions_while_opening_socket(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_handles_exceptions_while_binding_socket(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_opens_and_binds_socket(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_stores_message_of_new_client_and_new_aircraft(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_stores_message_of_existing_client_and_new_aircraft(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_stores_message_of_existing_client_and_existing_aircraft(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_queues_aircraft_image_download(self):
        pass

    @unittest.skip('Incomplete')
    def test_handle_handles_keyboard_interrupt(self):
        pass
