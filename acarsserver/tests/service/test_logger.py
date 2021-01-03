import logging
import unittest

from acarsserver.service.logger import LoggerService


class LoggerServiceTestCase(unittest.TestCase):
    logger = None

    def setUp(self):
        self.logger = LoggerService()

    def test_init_sets_level_and_handlers(self):
        logger = LoggerService()
        self.assertEqual(logging.DEBUG, logger.get_instance().level)

    def test_get_instance_returns_instance(self):
        logger = LoggerService()
        self.assertEqual('LoggerService', type(logger).__name__)
