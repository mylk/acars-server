from acarsserver.model.aircraft import Aircraft
from acarsserver.mapper.db.message import MessageDbMapper


class AircraftDbMapper:

    adapter = None

    def __init__(self, adapter):
        self.adapter = adapter

    def insert(self, aircraft):
        self.adapter.execute(
            'INSERT INTO aircrafts (registration, image, first_seen, last_seen) VALUES (?, ?, ?, ?)',
            (aircraft.registration, aircraft.image, aircraft.first_seen, aircraft.last_seen)
        )

        self.adapter.connection.commit()

    def fetch(self, id):
        self.adapter.execute('SELECT id, registration, image, first_seen, last_seen FROM aircrafts WHERE id = ?', (id,))
        result = self.adapter.fetchone()

        aircraft = None
        if result:
            aircraft = Aircraft(result)

        return aircraft

    def fetch_all(self, order=None, limit=None):
        # default order and limit, if not set
        order = ('id', 'ASC') if order is None else order
        limit = -1 if limit is None else limit

        # the actual query
        self.adapter.execute(
            """
                SELECT id, registration, image,
                strftime("%Y-%m-%d %H:%M:%S", "first_seen", "localtime") AS first_seen,
                strftime("%Y-%m-%d %H:%M:%S", "last_seen", "localtime") AS last_seen
                FROM aircrafts
                ORDER BY {} {} LIMIT {}
            """.format(
                order[0],
                order[1],
                limit
            )
        )
        results = self.adapter.fetchall()

        # map to models
        aircrafts = []
        for result in results:
            messages = MessageDbMapper(self.adapter).fetch_by('aircraft_id', result[0], ('created_at', 'DESC'))
            aircraft = Aircraft(result, messages)

            aircrafts.append(aircraft)

        return aircrafts

    def update(self, aircraft):
        self.adapter.execute(
            'UPDATE aircrafts SET image = ?, last_seen = ? WHERE id = ?',
            (aircraft.image, aircraft.last_seen, aircraft.id)
        )

        self.adapter.connection.commit()
