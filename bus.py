
class Bus():
    def __init__(self, bus_id, current_station, boarded_customers):
        self.bus_id = bus_id
        self.current_station = current_station
        self.boarded_customers = boarded_customers

    # For debugging purposes:
    def __str__(self):
        return f'Bus number {self.bus_id} is currently at station {self.current_station.station_id}'