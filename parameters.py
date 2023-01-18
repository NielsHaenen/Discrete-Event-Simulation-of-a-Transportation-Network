import random
from scipy.stats import expon
from station import Station


class Parameters:
    '''Initialize the parameter setting for our model, parameter setting can be 
    modified according to the user's preference'''
    def __init__(self, nr_buses):
        self.nr_of_buses = nr_buses
        self.capacity_bus = 100
        self.delay_prop = 0.1
        self.station_names = ['A', 'B', 'C', 'D']
        self.next_station = {'A':'B', 'B':'C', 'C':'D', 'D':'A'}
        self.travel_time_dict = {'A':720, 'B':900, 'C':1020, 'D':840}
        self.routing_dict = {'A':{'B':0.20, 'C':0.45,'D':0.35}, 
                             'B':{'A':0.15, 'C':0.35,'D':0.50},
                             'C':{'A':0.55, 'B':0.15,'D':0.30},
                             'D':{'A':0.40, 'B':0.35,'C':0.25}}

    '''The number or arrivals per day at each station is modeled dynamically with similar values over the day'''
    def intArrTime(self, day_time, station):
        if day_time < 3600:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 7200:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 10800:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 14400:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 18000:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 21600:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 25200:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 28800:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 32400:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 36000:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 39600:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        elif day_time < 43200:
            arr_dict = {'A':180,'B':175,'C':145,'D':150}
        station_id = station.station_id
        return round(1/(arr_dict[station_id]/3600), 4)

    def boardingTime(self):
        random_nr = random.random()
        if random_nr < self.delay_prop:
            boarding_time = 190 # 3 min + 10 seconds delay
        else:
            boarding_time = 180 # Regular 3 min boarding
        return boarding_time
        
    def findDestStation(self, origin_station_id):
        props = self.routing_dict
        dest_ids = list(props[origin_station_id].keys())
        dest_probs = list(props[origin_station_id].values())
        destination_station = random.choices(dest_ids, weights=dest_probs)[0]
        return destination_station