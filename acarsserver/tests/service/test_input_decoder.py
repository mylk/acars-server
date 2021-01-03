import unittest

from acarsserver.service.input_decoder import InputDecoderService


class InputDecoderServiceTestCase(unittest.TestCase):
    decoder = None

    def setUp(self):
        self.decoder = InputDecoderService()

    def test_get_decoder_returns_decoder(self):
        decoder = self.decoder.get_decoder()
        self.assertEqual('JSONDecoder', type(decoder).__name__)
