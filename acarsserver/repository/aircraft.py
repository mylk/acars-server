from acarsserver.model.aircraft import Aircraft


class AircraftRepository:

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def fetch_identical(self, aircraft):
        self.adapter.execute(
            """
                SELECT id, registration, image, first_seen, last_seen
                FROM aircrafts
                WHERE registration = ?
            """,
            (aircraft.registration,)
        )
        result = self.adapter.fetchone()

        aircraft = None
        if result:
            aircraft = Aircraft(result)

        return aircraft
