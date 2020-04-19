import json


class InputDecoderService:

    def get_decoder(self):
        return json.JSONDecoder(strict=False)
