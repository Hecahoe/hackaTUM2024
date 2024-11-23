import math

from priorityqueue import PriorityQueue


class Fleetmanager:
    def __init__(self, customers, vehicles):
        self.customers = {c.id: c for c in customers}
        self.vehicles = {v.id: v for v in vehicles}

    def set_customers(self, customers):
        self.customers = {c.id: c for c in customers}

    def set_vehicles(self, vehicles):
        self.vehicles = {v.id: v for v in vehicles}

    def get_waiting_customers(self):
        waiting_customers = {}
        vehicle_customerIds = [v.customerId for v in self.vehicles.values()]
        for c in self.customers.values():
            if c.awaitingService and c.id not in vehicle_customerIds:
                waiting_customers[c.id] = c
        return waiting_customers

    def get_available_vehicles(self):
        avail_vehics = {}
        for v in self.vehicles.values():
            if v.isAvailable:
                avail_vehics[v.id] = v
        return avail_vehics

    def build_heap(self):
        heaps = {}
        waiting_customers = self.get_waiting_customers()
        for v_id, v in self.get_available_vehicles().items():
            heaps[v_id] = PriorityQueue(
                {
                    haversine((c.coordX, c.coordY), (v.coordX, v.coordY)): c.id
                    for c in waiting_customers.values()
                }
            )
        return heaps

    def get_updates(self):
        updates = []
        heaps = self.build_heap()
        assigned_customers = set()
        for v in self.get_available_vehicles().values():
            heap = heaps[v.id]
            customer_id = None
            while customer_id not in assigned_customers and not heap.is_empty():
                customer_id = heap.get_smallest()
            if customer_id is not None:
                updates.append((v.id, customer_id))
                assigned_customers.add(customer_id)
        return updates


def haversine(coord1, coord2):
    # radius of earth
    R = 6371.0

    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
