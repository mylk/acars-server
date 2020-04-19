from unittest import TestCase
from webtest import TestApp

import helper


class IndexControllerTestCase(TestCase):

    def test_index(self):
        app = TestApp(helper.get_app())
        assert app.get('/').status == '200 OK'
