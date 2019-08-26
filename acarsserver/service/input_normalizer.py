class InputNormalizerService:

    @staticmethod
    def normalize(data):
        # some messages do not contain text
        if not 'text' in data:
            data['text'] = None

        return data
