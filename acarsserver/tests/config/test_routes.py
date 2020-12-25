import bottle
import inspect
import unittest

from acarsserver.app.controllers.index_controller import IndexController
from acarsserver.config import routes


class RoutesTestCase(unittest.TestCase):

    def test_setup_routing_sets_routes(self):
        app = bottle.Bottle()

        routes.setup_routing(app)

        self.assertIsNotNone(app.routes)
        self.assertTrue(len(app.routes) > 0)

        # last routes in index routes
        self.assertIs(IndexController.index, getattr(app.routes[-1].callback, '__func__'))
