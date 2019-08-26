import json


class InputDecoderService:

    def get_decoder():
        return json.JSONDecoder(strict=False)
