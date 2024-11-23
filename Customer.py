
class Customer:
    def __init__(self, customer_id: str, coordX: float, coordY: float, destinationX: float, destinationY: float):
        self.id = customer_id
        self.coordX = coordX
        self.coordY = coordY
        self.destinationX = destinationX
        self.destinationY = destinationY
        self.awaitingService = True

    def __repr__(self):
        return f"Customer(id={self.id}, coordX={self.coordX}, coordY={self.coordY}, destination=({self.destinationX}, {self.destinationY}))"


    #
    # def enter(self):
    #     self.awaitingService = False
    #
    # def leave(self):
    #     self.arrivedAtDestination = True