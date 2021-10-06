import mock
import unittest

import acarsserver.cli.client
from acarsserver.config import environment
from acarsserver.config import settings
from acarsserver.service.logger import LoggerService


class ClientTestCase(unittest.TestCase):

    client = None

    def setUp(self):
        self.client = acarsserver.cli.client
        self.client.os = mock.MagicMock()
        self.client.sys.exit = mock.MagicMock()

    def tearDown(self):
        self.client.LoggerService = LoggerService

    def test_init_sets_logger(self):
        client = self.client.Client()
        self.assertEqual('RootLogger', type(client.logger).__name__)

    def test_init_sets_configuration(self):
        client = self.client.Client()
        self.assertEquals(environment.listener_host, client.HOST)
        self.assertEquals(environment.listener_port, client.PORT)

    def test_handle_handles_os_error_while_executing_command(self):
        self.client.LoggerService = mock.MagicMock()
        self.client.os.execlp = mock.MagicMock(side_effect=OSError)
        # allow handle() to exit gracefully, otherwise the execution continues and test fails
        self.client.sys.exit = mock.MagicMock(side_effect=SystemExit)

        try:
            client = self.client.Client()
            client.handle()
        except SystemExit:
            pass

        client.logger.error.assert_called_once()
        self.client.sys.exit.assert_called_once()

    def test_handle_handles_keyboard_interrupt_while_executing_command(self):
        self.client.LoggerService = mock.MagicMock()
        self.client.os.execlp = mock.MagicMock(side_effect=KeyboardInterrupt)
        # allow handle() to exit gracefully, otherwise the execution continues and test fails
        self.client.sys.exit = mock.MagicMock(side_effect=SystemExit)

        try:
            client = self.client.Client()
            client.handle()
        except SystemExit:
            pass

        client.logger.warning.assert_called_with('Exiting gracefully.')
        self.client.sys.exit.assert_called_once()

    def test_handle_handles_system_exit_while_executing_command(self):
        self.client.LoggerService = mock.MagicMock()
        self.client.os.execlp = mock.MagicMock(side_effect=SystemExit)
        # allow handle() to exit gracefully, otherwise the execution continues and test fails
        self.client.sys.exit = mock.MagicMock(side_effect=SystemExit)

        try:
            client = self.client.Client()
            client.handle()
        except SystemExit:
            pass

        client.logger.warning.assert_called_with('Exiting gracefully.')
        self.client.sys.exit.assert_called_once()

    def test_handle_executes_command(self):
        self.client.LoggerService = mock.MagicMock()
        self.client.os.execlp = mock.MagicMock()

        client = self.client.Client()
        client.handle()

        self.assertEquals(3, client.logger.info.call_count)
        client.logger.warning.assert_not_called()
        client.logger.error.assert_not_called()
        self.client.os.execlp.assert_called_once_with(
            'acarsdec',
            '-A', '-j',
            '{}:{}'.format(environment.listener_host, environment.listener_port),
            '-o0',
            '-r',
            '0',
            *settings.acars_frequencies
        )
