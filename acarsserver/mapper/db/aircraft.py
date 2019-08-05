from acarsserver.model.aircraft import Aircraft


class AircraftDbMapper:

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def insert(self, aircraft):
        self.adapter.execute(
            'INSERT INTO aircrafts (registration, image) VALUES (?, ?)',
            (aircraft.registration, aircraft.image)
        )

        self.adapter.connection.commit()

    def fetch(self, id):
        self.adapter.execute('SELECT id, registration, image FROM aircrafts WHERE id = ?', (id,))
        result = self.adapter.fetchone()

        aircraft = None
        if result:
            aircraft = Aircraft(result)

        return aircraft

    def update(self, aircraft, image):
        self.adapter.execute(
            'UPDATE aircrafts SET image = ? WHERE id = ?',
            (image, aircraft.id)
        )

        self.adapter.connection.commit()
