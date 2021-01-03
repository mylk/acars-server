import unittest

from acarsserver.service.input_normalizer import InputNormalizerService


class InputNormalizerServiceTestCase(unittest.TestCase):
    normalizer = None

    def setUp(self):
        self.normalizer = InputNormalizerService()

    def test_normalize_adds_empty_text_element_when_not_exists(self):
        data = {
            'foo': 'bar',
        }

        expected = {
            'foo': 'bar',
            'text': None
        }

        actual = self.normalizer.normalize(data)
        self.assertEqual(expected, actual)

    def test_normalize_does_not_update_text_element_when_exists(self):
        data = {
            'foo': 'bar',
            'text': 'baz'
        }

        actual = self.normalizer.normalize(data)
        self.assertEqual(data, actual)
