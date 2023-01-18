class Station():
    def __init__(self, station_id, customer_queue, bus_queue):
        self.station_id = station_id
        self.customer_queue = customer_queue
        self.bus_queue = bus_queue

    # For debugging purposes:
    def __str__(self):
        return f'Station {self.station_id} has a bus queue of {len(self.bus_queue)} buses and {len(self.customer_queue)} customers waiting at the station'