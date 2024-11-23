from sitecustomize import cellar_prefix


class Fleetmanager:
    def __init__(self, customers, vehicles):
        self.customers = customers
        self.vehicles = vehicles

    def get_waiting_customers(self) -> list:
        waiting_customers = []
        vehicle_customerIds = [v.customerId for v in self.vehicles]
        for c in self.customers:
            if c.id not in vehicle_customerIds and c.awaitingService:
                waiting_customers.append(c)
        return waiting_customers

    def get_available_vehicles(self):
        avail_vehics = []
        for v in self.vehicles:
            if v.isAvailable:
                avail_vehics.append(v)
        return avail_vehics


    def algorithm(self):
        return None
