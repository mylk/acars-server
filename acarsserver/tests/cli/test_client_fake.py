import mock
import unittest

import acarsserver.cli.client_fake
from acarsserver.service.logger import LoggerService


class ClientFakeTestCase(unittest.TestCase):

    client_fake = None

    def setUp(self):
        self.client_fake = acarsserver.cli.client_fake
        self.client_fake.sys.exit = mock.MagicMock()

    def tearDown(self):
        self.client_fake.LoggerService = LoggerService

    def test_init_sets_logger(self):
        client_fake = self.client_fake.ClientFake()
        self.assertEqual('RootLogger', type(client_fake.logger).__name__)

    @mock.patch('socket.socket', side_effect=OSError)
    def test_handle_handles_os_error_while_creating_socket(self, mock_socket):
        self.client_fake.LoggerService = mock.MagicMock()
        # allow handle() to exit gracefully, otherwise the execution continues and test fails
        self.client_fake.sys.exit = mock.MagicMock(side_effect=SystemExit)

        try:
            client_fake = self.client_fake.ClientFake()
            client_fake.handle()
        except SystemExit:
            pass

        client_fake.logger.error.assert_called_once()
        self.client_fake.sys.exit.assert_called_once()

    @mock.patch('socket.socket.sendto', side_effect=KeyboardInterrupt)
    @mock.patch('socket.socket.close')
    def test_handle_handles_keyboard_interrupt_while_sending_data(self, mock_close, mock_sendto):
        self.client_fake.LoggerService = mock.MagicMock()

        client_fake = self.client_fake.ClientFake()
        client_fake.handle()

        client_fake.logger.info.assert_called_once()
        client_fake.logger.error.assert_not_called()
        client_fake.logger.warning.assert_called_with('Exiting gracefully.')
        mock_close.assert_called_once()

    @mock.patch('socket.socket.sendto', side_effect=SystemExit)
    @mock.patch('socket.socket.close')
    def test_handle_handles_system_exit_while_sending_data(self, mock_close, mock_sendto):
        self.client_fake.LoggerService = mock.MagicMock()

        client_fake = self.client_fake.ClientFake()
        client_fake.handle()

        client_fake.logger.info.assert_called_once()
        client_fake.logger.error.assert_not_called()
        client_fake.logger.warning.assert_called_with('Exiting gracefully.')
        mock_close.assert_called_once()

    @mock.patch('socket.socket.sendto', side_effect=OSError)
    @mock.patch('socket.socket.close')
    def test_handle_handles_os_error_while_sending_data(self, mock_close, mock_sendto):
        self.client_fake.LoggerService = mock.MagicMock()
        self.client_fake.sys.exit = mock.MagicMock(side_effect=SystemExit)

        try:
            client_fake = self.client_fake.ClientFake()
            client_fake.handle()
        except SystemExit:
            pass

        client_fake.logger.info.assert_called_once()
        client_fake.logger.error.assert_called_once()
        mock_close.assert_not_called()

    @mock.patch('socket.socket.sendto', side_effect=KeyboardInterrupt)
    @mock.patch('socket.socket.close')
    def test_handle_sends_data(self, mock_close, mock_sendto):
        self.client_fake.LoggerService = mock.MagicMock()

        client_fake = self.client_fake.ClientFake()
        client_fake.handle()

        mock_sendto.assert_called_once()
        mock_close.assert_called_once()
