from datetime import datetime


class Message:

    aircraft = None
    aircraft_image = None
    flight = None
    received_at = None

    def __str__(self):
        return 'Aircraft: {}, Flight: {}, Received At:{}, Aircraft Image:{}'.format(
            self.aircraft,
            self.flight,
            self.received_at.strftime('%Y-%m-%d %H:%M:%S'),
            self.aircraft_image
        )
