import numpy as np

class Results:
    def __init__(self):
        self.customer_events = []
        self.queue1_lengths = [(0, 0)] # Corresponding to station id and time
        self.queue2_lengths = [(0, 0)]
        self.queue3_lengths = [(0, 0)]
        self.queue4_lengths = [(0, 0)]
        self.boarding_ratio1 = []
        self.boarding_ratio2 = []
        self.boarding_ratio3 = []
        self.boarding_ratio4 = []
        
    def findRouteProbabilities(self):
        '''This method is only used to check whether our model is correct.
        The obtained route probabilities should allign with distribution 
        given in the parameters class
        '''
        stations = ['A', 'B', 'C', 'D']
        route_counter = dict()
        for station_1 in stations:
            for station_2 in stations:
                if station_1 != station_2:
                    route_counter[f'route {station_1} to {station_2}'] = 0
        for event in self.customer_events:
            origin = event[1]
            dest = event[2]
            route_counter[f'route {origin} to {dest}'] += 1
        
        nr_customer_from_1 = len([event for event in self.customer_events if event[1]=='A'])
        nr_customer_from_2 = len([event for event in self.customer_events if event[1]=='B'])
        nr_customer_from_3 = len([event for event in self.customer_events if event[1]=='C'])
        nr_customer_from_4 = len([event for event in self.customer_events if event[1]=='D'])
        
        for key, value in route_counter.items():
            if key[6]=='A':
                route_counter[key] = round(value/nr_customer_from_1, 3)
            if key[6]=='B':
                route_counter[key] = round(value/nr_customer_from_2, 3)
            if key[6]=='C':
                route_counter[key] = round(value/nr_customer_from_3, 3)
            if key[6]=='D':
                route_counter[key] = round(value/nr_customer_from_4, 3)
        return route_counter

    def registerCustomerData(self, leaving_customers:list):
        '''Registers info of customers to calculate relevant performance indicators'''
        for customer in leaving_customers:
            id = customer.customer_id
            origin_location = customer.origin_location
            destination_location = customer.destination_location
            arrival_time = customer.arrival_time
            boarding_time = customer.boarding_time
            departure_time = customer.departure_time
            self.customer_events.append([id, origin_location, destination_location, arrival_time,boarding_time, departure_time])
    
    def registerQueueLength(self, station, time):
        '''Registers queue length at each station'''
        station_id = station.station_id
        queue_length = len(station.customer_queue)
        if station_id == 'A':
            self.queue1_lengths.append((queue_length, time))
        elif station_id == 'B':
            self.queue2_lengths.append((queue_length, time))
        elif station_id == 'C':
            self.queue3_lengths.append((queue_length, time))
        elif station_id == 'D':
            self.queue4_lengths.append((queue_length, time))

    def registerBoardingInfo(self, station, fraction_boarded):
        '''Registers for each station the fraction of the queue that is boarded'''
        station_id = station.station_id
        if station_id == 'A':
            self.boarding_ratio1.append(fraction_boarded)
        elif station_id == 'B':
            self.boarding_ratio2.append(fraction_boarded)
        elif station_id == 'C':
            self.boarding_ratio3.append(fraction_boarded)
        elif station_id == 'D':
            self.boarding_ratio4.append(fraction_boarded)

    def getWaitingTimeStatistics(self):
        '''Calculates the expected waiting time at each station'''
        events = self.customer_events
        
        events_q1 = [event for event in events if event[1]=='A']
        waiting_time_dict1 = {f'Customer {event[0]}':round(event[4]-event[3], 1) for event in events_q1}
        exp_w_time_q1 = round(sum(waiting_time_dict1.values()) / len(waiting_time_dict1), 1)
        
        events_q2 = [event for event in events if event[1]=='B']
        waiting_time_dict2 = {f'Customer {event[0]}':round(event[4]-event[3], 1) for event in events_q2}
        exp_w_time_q2 = round(sum(waiting_time_dict2.values()) / len(waiting_time_dict2), 1)
        
        events_q3 = [event for event in events if event[1]=='C']
        waiting_time_dict3 = {f'Customer {event[0]}':round(event[4]-event[3], 1) for event in events_q3}
        exp_w_time_q3 = round(sum(waiting_time_dict3.values()) / len(waiting_time_dict3), 1)
        
        events_q4 = [event for event in events if event[1]=='D']
        waiting_time_dict4 = {f'Customer {event[0]}':round(event[4]-event[3], 1) for event in events_q4}
        exp_w_time_q4 = round(sum(waiting_time_dict4.values()) / len(waiting_time_dict4), 1)
        
        exp_waiting_times = {'Exp_W_Q1': exp_w_time_q1, 'Exp_W_Q2': exp_w_time_q2, 'Exp_W_Q3': exp_w_time_q3, 'Exp_W_Q4': exp_w_time_q4}
        return exp_waiting_times
    
    def getExpectedQueueLengths(self):
        '''Calculates the expected queue length at each queue'''
        exp_queue_lengths = dict()
        last_boarding_time = self.customer_events[-1][4]
        for queue_index, queue_info in enumerate([self.queue1_lengths, self.queue2_lengths, self.queue3_lengths, self.queue4_lengths]):
            queue_info_new = list(filter(lambda x: x[1]<=last_boarding_time, queue_info))
            queue_lengths = [queue_length for queue_length, time in queue_info_new]
            different_queue_lengths = np.unique(queue_lengths)
            time_per_queue__length_dict = {str(length):0 for length in different_queue_lengths}

            for index in range(len(queue_info_new)-1):
                length = str(queue_info_new[index][0])
                delta_time = queue_info_new[index+1][1] - queue_info_new[index][1]
                time_per_queue__length_dict[length] += delta_time
            probability_per_queue__length_dict = dict()
            for key, value in time_per_queue__length_dict.items():
                probability_per_queue__length_dict[key] = time_per_queue__length_dict[key]/last_boarding_time
            expected_queue_length = 0
            for key, value in probability_per_queue__length_dict.items():
                expected_queue_length += int(key)*value
            exp_queue_lengths[f'Exp_L_Q{queue_index+1}'] = round(expected_queue_length)
        return exp_queue_lengths
    
    def getBoardingProbabilities(self):
        '''Calculates for each station the average probability that a customer will be boarded'''
        prob1 = round(np.mean(self.boarding_ratio1)*100, 2)
        prob2 = round(np.mean(self.boarding_ratio2)*100, 2)
        prob3 = round(np.mean(self.boarding_ratio3)*100, 2)
        prob4 = round(np.mean(self.boarding_ratio4)*100, 2)
        prob_per_station_dict = {'Probability station A': prob1, 'Probability station B': prob2, 'Probability station C': prob3, 'Probability station D': prob4}
        return prob_per_station_dict