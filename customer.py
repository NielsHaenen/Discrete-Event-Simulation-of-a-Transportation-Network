class Customer():
    
    def __init__(self, customer_id, origin_location:str, destination_location:str, arrival_time, boarding_time=None, departure_time=None):
        self.customer_id = customer_id
        self.origin_location = origin_location
        self.destination_location = destination_location
        self.arrival_time = arrival_time
        self.boarding_time = boarding_time
        self.departure_time = departure_time

    # For debugging purposes:
    def __str__(self):
            return f'Customer number {self.customer_id} traveling from {self.origin_location} to {self.destination_location}'