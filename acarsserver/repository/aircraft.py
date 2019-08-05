from acarsserver.model.aircraft import Aircraft


class AircraftRepository:

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def fetch_identical(self, aircraft):
        self.adapter.execute('SELECT id, registration, image FROM aircrafts WHERE registration = ?', (aircraft.registration,))
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
