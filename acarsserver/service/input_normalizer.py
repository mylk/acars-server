class InputNormalizerService:

    @staticmethod
    def normalize(data):
        # some messages do not contain text
        if 'text' not in data:
            data['text'] = None

        return data
