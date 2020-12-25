import importlib
import os
import unittest

from acarsserver.config import environment


class EnvironmentTestCase(unittest.TestCase):

    def test_main_throws_exception_when_environment_not_set(self):
        del os.environ['ENV']

        exception_thrown = False
        try:
            importlib.reload(environment)
        except RuntimeError:
            exception_thrown = True

        self.assertTrue(exception_thrown)

    def test_main_throws_exception_when_environment_is_invalid(self):
        os.environ['ENV'] = 'foo'

        exception_thrown = False
        try:
            importlib.reload(environment)
        except RuntimeError:
            exception_thrown = True

        self.assertTrue(exception_thrown)

    def test_main_sets_configuration_of_production_environment(self):
        os.environ['ENV'] = 'production'

        importlib.reload(environment)

        self.assertEqual('mylk.wtf', environment.listener_host)

    def test_main_sets_configuration_of_development_environment(self):
        os.environ['ENV'] = 'development'

        importlib.reload(environment)

        self.assertEqual('listener', environment.listener_host)

    def test_main_sets_configuration_of_test_environment(self):
        os.environ['ENV'] = 'test'

        importlib.reload(environment)

        self.assertEqual('localhost', environment.listener_host)
