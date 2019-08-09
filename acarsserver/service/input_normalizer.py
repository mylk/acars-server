class InputNormalizerService:

    @staticmethod
    def normalize(data):
        # acarsdec has different output if the messages
        # are sent to a remote or local host.
        if not data[1] is '':
            data.insert(1, '')

        # some private aircrafts have an extra field
        # in place of the aircraft registration id.
        if data[10] is '':
            del data[10]

        return data
