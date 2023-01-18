import random
import time
import pandas as pd
from scipy.stats import expon

from customer import Customer
from results import Results
from event import Event
from fes import FES
from parameters import Parameters
from station import Station
from bus import Bus

class Simulation():
    def __init__(self, nr_buses):
        self.par = Parameters(nr_buses)
        self.res = Results()
        self.fes = FES()
        
        self.capacity_bus = self.par.capacity_bus
        
        self.sim_day = 0
        self.event_id = 0
        self.customer_id = 0
    
        # Create list with station objects
        self.station_list = [Station(station_id=station_name,
                                     customer_queue=[],
                                     bus_queue=[]) for station_name in self.par.station_names]
        
        # Create list with bus objects
        self.bus_list = [Bus(bus_id=bus_nr, 
                                 current_station=random.choice(self.station_list),
                                 boarded_customers=[]) for bus_nr in range(1, self.par.nr_of_buses+1)]
        
         # Randomly allocate buses to stations
        for station in self.station_list:
            bus_queue_at_station = [bus for bus in self.bus_list if bus.current_station == station]
            station.bus_queue = bus_queue_at_station

    def continueSim(self):
        '''Check whether the simulation should keep running'''
        no_waiting_customers, no_boarded_customers, late = False, False, False
        if all(not station.customer_queue for station in self.station_list):
            no_waiting_customers = True
        if all(not bus.boarded_customers for bus in self.bus_list):
            no_boarded_customers = True
        if self.day_time >= 43200:
            late = True
        # Stop running if the parc is closed and there are no customers waiting and no customers boarded
        if no_waiting_customers and no_boarded_customers and late:
            return False
        else:
            return True

    def newCusArrEvent(self, station):
        curr_time = self.day_time
         # No new arrival event is scheduled if parc is closed
        if curr_time >= 43200:
            return None
        inter_arrival_time = self.par.intArrTime(curr_time, station)
        event_time = curr_time + expon.rvs(inter_arrival_time)

        event_type = 'CUST_ARR'
        event = Event(event_id=self.event_id,
                      time=event_time,
                      type=event_type,
                      station=station)
        self.event_id += 1
        return event

    def newBusArrEvent(self, station, bus):
        travel_time = self.par.travel_time_dict
        curr_time = self.day_time
        station_id = station.station_id
        if not self.continueSim():
            return None # No new leaving event is scheduled if parc is closed and no customers are in the bus
        event_time = curr_time + travel_time[station_id]
        event_type = 'BUS_ARRIVAL'
        event = Event(event_id=self.event_id,
                      time=event_time,
                      type=event_type,
                      station=station,
                      bus=bus)
        self.event_id += 1
        return event
            
    def newBusDepEvent(self, station, bus):
        curr_time = self.day_time
        if not self.continueSim():
            return None # No new leaving event is scheduled if parc is closed and no customers are in the bus
        event_time = curr_time + self.par.boardingTime()
        event_type = 'BUS_DEPARTURE'
        event = Event(event_id=self.event_id,
                      time=event_time,
                      type=event_type,
                      station=station,
                      bus=bus)
        self.event_id += 1
        return event
    
    def updatePropertiesCustomerArr(self, station):
        destination = self.par.findDestStation(station.station_id)
        new_customer = Customer(customer_id=self.customer_id,
                                origin_location=station.station_id,
                                destination_location=destination,
                                arrival_time=self.day_time
                                )
        self.customer_id += 1
        station.customer_queue.append(new_customer)
        self.res.registerQueueLength(station, self.day_time)

    def updatePropertiesBusDep(self, station, bus):
        '''Used to update objects when there is a bus departure'''
        len_queue_before = len(station.customer_queue)
        bus.current_station = station
        station.bus_queue.pop(0) # Remove bus from bus queue at departure 
        # Keep adding customers to bus till the bus is full or customer queue is empty 
        while len(bus.boarded_customers) < self.capacity_bus and len(station.customer_queue) > 0:
            new_customer = station.customer_queue.pop(0)
            new_customer.boarding_time = self.day_time # Register customer boarding time for analysis
            bus.boarded_customers.append(new_customer)
        len_queue_after = len(station.customer_queue)
        if len_queue_before: # Avoid division by zero if there is no queue
            fraction_boarded = (len_queue_before-len_queue_after)/len_queue_before
            self.res.registerBoardingInfo(station, fraction_boarded)
        self.res.registerQueueLength(station, self.day_time)
        
        
    def updatePropertiesBusArr(self, station, bus):
        '''Used to update objects when a bus arri'''
        leaving_customers = list(filter(lambda customer: customer.destination_location == station.station_id, bus.boarded_customers)) # List of customer that arrived at destination
        for customer in leaving_customers:
            customer.departure_time = self.day_time # Register customer departure time for analysis
        self.res.registerCustomerData(leaving_customers)
        bus.boarded_customers = list(filter(lambda customer: customer.destination_location != station.station_id, bus.boarded_customers)) # Boarded customers are those that did not arrived at their desitnation yet
        
    def scheduleFirstEvents(self):
        # Schedule leaving event at the stations where there is a bus
        for station in self.station_list:
            if station.bus_queue:
                bus_dep_event = self.newBusDepEvent(station, station.bus_queue[0])
                self.fes.add(bus_dep_event)
        # Schedule first customer arrival events at each station
        for station in self.station_list:
            cus_arr_event = self.newCusArrEvent(station)
            self.fes.add(cus_arr_event)
    
    def simulateDay(self):
        event = self.fes.next()
        self.day_time = event.time # The current time during the day
        current_station = event.station # The station where the event takes place
        current_bus = event.bus # The bus that is related to the event
        
        # In case the next event is a customer arrival
        if event.type == 'CUST_ARR':
            self.updatePropertiesCustomerArr(current_station) # Create customer and add it to the queue
            cus_arr_event = self.newCusArrEvent(current_station)
            self.fes.add(cus_arr_event) # Schedule next customer arrival event

        # In case the next event is a bus departure
        elif event.type == 'BUS_DEPARTURE':
            self.updatePropertiesBusDep(current_station, current_bus)
            # Schedule arrival event at next station
            station_id = current_station.station_id
            next_station = next((x for x in self.station_list if x.station_id == self.par.next_station[station_id]), None)
            bus_arr_event = self.newBusArrEvent(next_station, current_bus)
            self.fes.add(bus_arr_event) # Schedule next bus arrival event
            
            # Schedule new departure event if there is a queue at current station
            if current_station.bus_queue:
                next_bus = current_station.bus_queue[0] # First bus in bus queue
                self.updatePropertiesBusArr(current_station, next_bus)
                bus_dep_event= self.newBusDepEvent(current_station, next_bus)
                # print(next_bus.bus_id)
                self.fes.add(bus_dep_event) # Schedule next bus departure event
                
        # In case the next event is a bus arrival
        elif event.type == 'BUS_ARRIVAL':
                # In case there is no queue at the station where the bus arrives
            if not current_station.bus_queue:
                bus_dep_event = self.newBusDepEvent(current_station, current_bus)
                self.updatePropertiesBusArr(current_station, current_bus)
                self.fes.add(bus_dep_event) # Schedule bus departure event
            
            # In any case, we add the bus arrival to the queue
            current_station.bus_queue.append(current_bus)
        
    def run(self):
        start_time = time.time()
        self.day_time = 0
        self.scheduleFirstEvents() # Schedule the first events when new day starts

        # Each new day we run the simulation until the parc is closed and no customers need to be served
        running = True
        while running:
            self.simulateDay() # Simulate a new day
            if self.fes.is_empty(): # From running that day if the day if finished
                running = False
        self.simulation_time = round(time.time()-start_time, 2)
        
        'SIMULATION RESULTS'
        self.exp_queue_lengths = self.res.getExpectedQueueLengths()
        self.exp_waiting_times = self.res.getWaitingTimeStatistics()
        self.boarding_probabilities = self.res.getBoardingProbabilities()
        exp_queue_lengths = list(self.exp_queue_lengths.values())
        exp_waiting_times = list(self.exp_waiting_times.values())
        boarding_probabilities = list(self.boarding_probabilities.values())
        data = list(zip(exp_queue_lengths, exp_waiting_times, boarding_probabilities))
        self.simulation_results = pd.DataFrame({'Indicator': ['E[L]', 'E[W]', 'P[B]'], 'Station 1': data[0], 'Station 2': data[1], 'Station 3': data[2], 'Station 4': data[3]}, index=None).to_string(index=False)