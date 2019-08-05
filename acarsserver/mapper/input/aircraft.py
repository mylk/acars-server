from acarsserver.model.aircraft import Aircraft


class AircraftInputMapper:

    @staticmethod
    def map(registration):
        aircraft = Aircraft([None, registration, None])

        return aircraft
