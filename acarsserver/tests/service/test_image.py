from datetime import datetime
import json
import mock
import os
import unittest
from urllib import error

from acarsserver.adapter.sqlite import SqliteAdapter
from acarsserver.model.aircraft import Aircraft
from acarsserver.service import image
from acarsserver.service.logger import LoggerService


class ImageServiceTestCase(unittest.TestCase):

    adapter = None
    image_service = None
    logger = None
    seen_datetime = None

    def setUp(self):
        image.AircraftDbMapper.update = mock.MagicMock()
        image.Image = mock.MagicMock()
        image.json = mock.MagicMock()
        image.request = mock.MagicMock()

        self.adapter = SqliteAdapter().get_instance()
        self.logger = LoggerService().get_instance()
        self.image_service = image.ImageService(self.adapter, self.logger)
        self.seen_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    def test_init_sets_adapter_and_logger(self):
        adapter = self.image_service.adapter
        self.assertEqual('Cursor', type(adapter).__name__)

        logger = self.image_service.logger
        self.assertEqual('RootLogger', type(logger).__name__)

    def test_handle_does_nothing_when_aircraft_image_exists_locally(self):
        self.image_service.exists = mock.MagicMock(return_value=True)
        self.image_service.get_url = mock.MagicMock()

        aircraft = Aircraft([None, 'foo', 'foo.png', self.seen_datetime, self.seen_datetime])
        self.image_service.handle(aircraft)

        self.image_service.exists.assert_called_once()
        self.image_service.get_url.assert_not_called()

    def test_handle_does_nothing_when_aircraft_image_does_not_exist_locally_and_does_not_exist_online_too(self):
        self.image_service.exists = mock.MagicMock(return_value=False)
        self.image_service.get_url = mock.MagicMock(return_value=None)
        self.image_service.download_image = mock.MagicMock()

        aircraft = Aircraft([None, 'foo', 'foo.png', self.seen_datetime, self.seen_datetime])
        self.image_service.handle(aircraft)

        self.image_service.exists.assert_called_once()
        self.image_service.get_url.assert_called_once()
        self.image_service.download_image.assert_not_called()

    def test_handle_downloads_image_when_aircraft_image_does_not_exist_locally_and_exist_online(self):
        self.image_service.exists = mock.MagicMock(return_value=False)
        self.image_service.get_url = mock.MagicMock(return_value='http://www.google.com')
        self.image_service.download_image = mock.MagicMock()
        self.image_service.optimize = mock.MagicMock()
        self.image_service.create_thumbnail = mock.MagicMock()

        aircraft = Aircraft([None, 'foo', 'foo.png', self.seen_datetime, self.seen_datetime])
        self.image_service.handle(aircraft)

        self.assertEqual(1, self.image_service.exists.call_count)
        self.assertEqual(1, self.image_service.get_url.call_count)
        self.assertEqual(1, self.image_service.download_image.call_count)
        self.assertEqual(1, self.image_service.optimize.call_count)
        self.assertEqual(1, self.image_service.create_thumbnail.call_count)
        self.assertEqual(1, image.AircraftDbMapper.update.call_count)

    def test_exists_returns_false_when_image_does_not_exist_locally(self):
        aircraft = Aircraft([None, 'foo', 'foo', self.seen_datetime, self.seen_datetime])

        file_exists = self.image_service.exists(aircraft)

        self.assertFalse(file_exists)

    def test_exists_returns_true_when_image_exists_locally(self):
        aircraft = Aircraft([None, 'foo', 'paper_plane.png', self.seen_datetime, self.seen_datetime])

        file_exists = self.image_service.exists(aircraft)

        self.assertTrue(file_exists)

    def test_get_url_handles_exception_when_image_provider_returns_error(self):
        aircraft = Aircraft([None, 'bar', None, self.seen_datetime, self.seen_datetime])

        http_error = error.HTTPError('http://www.google.com', 404, 'foo', 'hdrs', mock.MagicMock())
        image.request.urlopen = mock.MagicMock(side_effect=http_error)
        url = self.image_service.get_url(aircraft)

        image.request.urlopen.assert_called_once_with(
            'https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&' +
            'gcmtitle=Category:bar_(aircraft)&gcmtype=file&redirects=1&prop=imageinfo&iiprop=url&format=json'
        )
        self.assertIsNone(url)
        image.json.loads.assert_not_called()

    def test_get_url_returns_none_when_image_provider_response_is_not_the_expected(self):
        aircraft = Aircraft([None, 'bar', None, self.seen_datetime, self.seen_datetime])

        response = mock.MagicMock()
        image.json.loads.return_value = json.loads('{"foo": "bar"}')
        image.request.urlopen = mock.MagicMock(return_value=response)
        url = self.image_service.get_url(aircraft)

        self.assertIsNone(url)
        image.json.loads.assert_called_once()
        # self.assertFalse(True)

    def test_get_url_returns_the_image_url_when_image_exists_online(self):
        aircraft = Aircraft([None, 'bar', None, self.seen_datetime, self.seen_datetime])

        path = os.path.dirname(os.path.realpath(__file__))
        with open('{}/../fixtures/aircraft_images.json'.format(path)) as fixture_file:
            fixture_data = fixture_file.read()
            fixture_file.close()

        response = mock.MagicMock()
        image.json.loads.return_value = json.loads(fixture_data)
        image.request.urlopen = mock.MagicMock(return_value=response)
        url = self.image_service.get_url(aircraft)

        self.assertEqual('https://upload.wikimedia.org/wikipedia/commons/2/2b/Continental_Airlines_Boeing_767-400%3B_N69059%40ZRH%3B16.07.2010_583bk_%284799578145%29.jpg', url)
        image.json.loads.assert_called_once()

    def test_download_image_handles_os_and_image_provider_errors(self):
        aircraft = Aircraft([None, 'bar', 'bar.png', self.seen_datetime, self.seen_datetime])

        image.request.urlretrieve = mock.MagicMock(side_effect=OSError)
        filename = self.image_service.download_image('http://foo.com/bar.png', aircraft)
        image.request.urlretrieve.assert_called_once_with(
            'http://foo.com/bar.png',
            '/acars-server/acarsserver/service/../app/assets/img/aircrafts/large/bar.png'
        )
        self.assertIsNone(filename)

        image.request.urlretrieve = mock.MagicMock(side_effect=error.URLError('Not Found'))
        filename = self.image_service.download_image('http://foo.com/bar.png', aircraft)
        image.request.urlretrieve.assert_called_once_with(
            'http://foo.com/bar.png',
            '/acars-server/acarsserver/service/../app/assets/img/aircrafts/large/bar.png'
        )
        self.assertIsNone(filename)

    def test_download_image_downloads_the_image(self):
        aircraft = Aircraft([None, 'bar', 'bar.png', self.seen_datetime, self.seen_datetime])

        filename = self.image_service.download_image('http://foo.com/bar.png', aircraft)

        image.request.urlretrieve.assert_called_once_with(
            'http://foo.com/bar.png',
            '/acars-server/acarsserver/service/../app/assets/img/aircrafts/large/bar.png'
        )

        self.assertEqual('bar.png', filename)

    def test_create_thumbnail_returns_false_when_file_format_could_not_be_identified(self):
        self.image_service.get_image_format = mock.MagicMock(return_value=False)

        result = self.image_service.create_thumbnail('foo.png')

        image.Image.open.assert_not_called()
        self.assertFalse(result)

    def test_create_thumbnail_handles_thumbnail_creation_exceptions_and_returns_false(self):
        self.image_service.get_image_format = mock.MagicMock(return_value='png')
        image.Image.open.side_effect = OSError

        result = self.image_service.create_thumbnail('foo.png')

        image.Image.open.assert_called_once()
        self.assertFalse(result)

    def test_create_thumbnail_creates_thumbnail_and_returns_true(self):
        mock_image = mock.MagicMock()

        self.image_service.get_image_format = mock.MagicMock(return_value='png')
        image.Image.open.return_value = mock_image

        result = self.image_service.create_thumbnail('foo.png')

        image.Image.open.assert_called_once()
        mock_image.thumbnail.assert_called_once()
        mock_image.save.assert_called_once()
        self.assertTrue(result)

    def test_optimize_returns_false_when_image_format_could_not_be_identified(self):
        self.image_service.get_image_format = mock.MagicMock(return_value=False)

        result = self.image_service.optimize('foo.png')

        image.Image.open.assert_not_called()
        self.assertFalse(result)

    def test_optimize_handles_optimization_exceptions_and_returns_false(self):
        self.image_service.get_image_format = mock.MagicMock(return_value='png')
        image.Image.open.side_effect = OSError

        result = self.image_service.optimize('foo.png')

        image.Image.open.assert_called_once()
        self.assertFalse(result)

    def test_optimize_optimizes_image_and_returns_true(self):
        mock_image = mock.MagicMock()

        self.image_service.get_image_format = mock.MagicMock(return_value='png')
        image.Image.open.return_value = mock_image

        result = self.image_service.optimize('foo.png')

        image.Image.open.assert_called_once()
        mock_image.save.assert_called_once()
        self.assertTrue(result)

    def test_get_image_format_handles_exception_and_returns_none(self):
        file_format = self.image_service.get_image_format('foo')

        self.assertIsNone(file_format)

    def test_get_image_format_returns_image_format(self):
        file_format = self.image_service.get_image_format('paper_plane.png')

        self.assertTrue('png', file_format)
