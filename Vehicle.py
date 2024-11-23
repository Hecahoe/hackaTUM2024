from typing import List, Optional

class Vehicle:
    def __init__(self, vehicle_id: str, coordX: float, coordY: float, vehicleSpeed: float):
        self.id = vehicle_id
        self.coordX = coordX
        self.coordY = coordY
        self.isAvailable = True
        self.vehicleSpeed = vehicleSpeed
        self.customerId: Optional[str] = None
        self.remainingTravelTime = 0.0
        self.distanceTravelled = 0.0
        self.activeTime = 0.0
        self.numberOfTrips = 0

    def __repr__(self):
        return f"Vehicle(id={self.id}, coordX={self.coordX}, coordY={self.coordY}, speed={self.vehicleSpeed})"

    # def load(self, vehicle_id: str, customer_id: str):
    #     self.id = vehicle_id
    #     self.customerId = customer_id
    #     self.isAvailable = False
    #
    #
    #
    # def unload(self, vehicle_id: str):
    #     self.id = vehicle_id
    #     self.isAvailable = True