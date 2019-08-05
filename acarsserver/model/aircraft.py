class Aircraft:

    id = None
    registration = None
    image = None

    def __init__(self, result):
        self.id = result[0]
        self.registration = result[1]
        self.image = result[2]

    def __str__(self):
        return 'ID: {}, Registration:{}, Image: {}'.format(
            self.id,
            self.registration,
            self.image
        )
