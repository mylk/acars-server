from webtest import TestApp
import unittest

from acarsserver.tests.app.controllers import helper


class IndexControllerTestCase(unittest.TestCase):

    def test_img_returns_image_data(self):
        app = TestApp(helper.get_app())
        response = app.get('/img/aircrafts/paper_plane.png')

        self.assertNotIn(b'Error: 404 Not Found', response.body)

    def test_img_returns_css_data(self):
        app = TestApp(helper.get_app())
        response = app.get('/css/application.css')

        self.assertNotIn(b'Error: 404 Not Found', response.body)

    def test_img_returns_js_data(self):
        app = TestApp(helper.get_app())
        response = app.get('/js/index.js')

        self.assertNotIn(b'Error: 404 Not Found', response.body)
