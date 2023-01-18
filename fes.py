import heapq

class FES:
    def __init__(self):
        self.events = []

    def add(self, event):
        if event:
            heapq.heappush(self.events, event)
        
    def next(self):
        return heapq.heappop(self.events)

    def is_empty(self):
        return True if not self.events else False

    # For debugging purposes:
    def __str__(self):
        event_list = []
        for event in self.events:
            event_list.append(str(event))
        return str(event_list)

