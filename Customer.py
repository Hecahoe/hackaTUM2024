class Customer:
    # def __init__(self, customer_id: str, coordX: float, coordY: float, destinationX: float, destinationY: float):
    #     self.id = customer_id
    #     self.coordX = coordX
    #     self.coordY = coordY
    #     self.destinationX = destinationX
    #     self.destinationY = destinationY
    #     self.awaitingService = True

    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

    # def __repr__(self):
    #     return f"Customer(id={self.id}, coordX={self.coordX}, coordY={self.coordY}, destination=({self.destinationX}, {self.destinationY}))"

    #
    # def enter(self):
    #     self.awaitingService = False
    #
    # def leave(self):
    #     self.arrivedAtDestination = True


def init_customers(customers):
    customers_new = []
    for c in customers:
        customers_new.append(Customer(c))
    return customers_new

