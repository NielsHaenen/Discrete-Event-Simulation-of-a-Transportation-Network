
class Event():
    '''Types:
    CUST_ARR
    BUS_ARRIVAL
    BUS_DEPARTURE
    '''
    def __init__(self, event_id, time, type, station=None, bus=None):
        self.event_id = event_id
        self.time = time
        self.type = type
        self.station = station
        self.bus = bus

    def __lt__(self, other):
        return self.time < other.time

    # For debugging purposes:
    def __str__(self):
        return f'Event nr {self.event_id} at time {round(self.time, 4)} of type {self.type} at station {self.station.station_id}'