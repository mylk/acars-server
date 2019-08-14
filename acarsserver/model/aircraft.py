class Aircraft:

    id = None
    registration = None
    image = None
    first_seen = None
    last_seen = None
    messages = []

    def __init__(self, result, messages=[]):
        self.id = result[0]
        self.registration = result[1]
        self.image = result[2]
        self.first_seen = result[3]
        self.last_seen = result[4]
        # relationship with messages
        self.messages = messages

    def __str__(self):
        return 'ID: {}, Registration: {}, Image: {}, First Seen: {}, Last Seen: {}'.format(
            self.id,
            self.registration,
            self.image,
            self.first_seen.strftime('%Y-%m-%d %H:%M:%S'),
            self.last_seen.strftime('%Y-%m-%d %H:%M:%S')
        )

    def __iter__(self):
        yield 'id', self.id
        yield 'registration', self.registration
        yield 'image', self.image
        yield 'first_seen', self.first_seen
        yield 'last_seen', self.last_seen
