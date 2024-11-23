import math
import random
from typing import List, Optional

import numpy as np
from scipy.optimize import linear_sum_assignment

import Customer
import Vehicle


class Scenario:
    def __init__(self, scenario_id: str, start_time: str, end_time: str):
        self.id = scenario_id
        self.startTime = start_time
        self.endTime = end_time
        self.status = "Initialized"
        self.vehicles: List[Vehicle] = []
        self.customers: List[Customer] = []

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)

    def add_customer(self, customer: Customer):
        self.customers.append(customer)

    def __repr__(self):
        return f"Scenario(id={self.id}, status={self.status}, vehicles={len(self.vehicles)}, customers={len(self.customers)})"

    @classmethod
    def initialize(cls, scenario_id: str, start_time: str, end_time: str, num_vehicles: int, num_customers: int):
        """
        Creates a scenario instance with the specified number of vehicles and customers.
        Coordinates are randomized between -200 and 200.
        """
        scenario = cls(scenario_id, start_time, end_time)

        # Randomly generate vehicles
        for i in range(num_vehicles):
            vehicle = Vehicle.Vehicle(
                vehicle_id=f"vehicle_{i + 1}",
                coordX=round(random.uniform(-200, 200), 2),
                coordY=round(random.uniform(-200, 200), 2),
                vehicleSpeed=round(random.uniform(30, 50), 2)  # Speed range: 30 to 70
            )
            scenario.add_vehicle(vehicle)

        # Randomly generate customers
        for i in range(num_customers):
            customer = Customer.Customer(
                customer_id=f"customer_{i + 1}",
                coordX=round(random.uniform(-200, 200), 2),
                coordY=round(random.uniform(-200, 200), 2),
                destinationX=round(random.uniform(-200, 200), 2),
                destinationY=round(random.uniform(-200, 200), 2)
            )
            scenario.add_customer(customer)

        return scenario




def test_case():
    scenario = Scenario(scenario_id="test_scenario", start_time="2024-11-22T10:00:00", end_time="2024-11-22T11:00:00")

    # Add 2 vehicles
    # scenario.add_vehicle(Vehicle.Vehicle(vehicle_id="vehicle_1", coordX=0, coordY=0, vehicleSpeed=50))
    # scenario.add_vehicle(Vehicle.Vehicle(vehicle_id="vehicle_2", coordX=100, coordY=100, vehicleSpeed=50))
    # scenario.add_vehicle(Vehicle(vehicle_id="vehicle_3", coordX=100, coordY=100, vehicleSpeed=50))
    # scenario.add_vehicle(Vehicle(vehicle_id="vehicle_4", coordX=100, coordY=100, vehicleSpeed=50))
    # scenario.add_vehicle(Vehicle(vehicle_id="vehicle_5", coordX=100, coordY=100, vehicleSpeed=50))
    #
    # # Add 3 customers
    # scenario.add_customer(Customer(customer_id="customer_1", coordX=5, coordY=5, destinationX=10, destinationY=10))
    # scenario.add_customer(Customer(customer_id="customer_2", coordX=95, coordY=95, destinationX=110, destinationY=110))
    # scenario.add_customer(Customer(customer_id="customer_3", coordX=50, coordY=50, destinationX=60, destinationY=60))

    vehicles = scenario.vehicles
    customers = scenario.customers

    # Optimize the allocation of vehicles to customers
    optimal_assignments = optimize_allocation(vehicles, customers)

    # Print the optimal assignments
    for vehicle_idx, customer_idx in optimal_assignments:
        print(f"Vehicle {vehicles[vehicle_idx].id} is assigned to Customer {customers[customer_idx].id}")

def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_travel_time(vehicle, future_costomer):
    travel_time = 0
    vehicle_x = vehicle.coordX
    vehicle_y = vehicle.coordY
    current_speed = vehicle.vehicleSpeed

    if not vehicle.isAvailable:
        current_customer = vehicle.customers[future_costomer.customer_id] #This will be a pull request "/customers/{customerId}"
        travel_time += calculate_distance(vehicle_x, vehicle_y, current_customer.destinationX, current_customer.destinationY) / current_speed
        travel_time += calculate_distance(current_customer.destinationX, current_customer.destinationY, future_costomer.coordX, future_costomer.coordY) / current_speed
    else:
        customer_x = future_costomer.coordX
        customer_y = future_costomer.coordY
        travel_time += calculate_distance(vehicle_x, vehicle_y, customer_x, customer_y) / current_speed

    return travel_time




def calculate_cost_matrix(vehicles, customers):

    #filter customers that awaitingService == False


    num_vehicles = len(vehicles)
    num_customers = len(customers)
    # Initialize cost matrix with distances
    cost_matrix = np.zeros((num_vehicles, num_customers))
    for i, vehicle in enumerate(vehicles):
        for j, customer in enumerate(customers):

            cost_matrix[i, j] = (
                calculate_distance(vehicle.coordX, vehicle.coordY, customer.coordX, customer.coordY))

    # If the matrix is not square
    if num_vehicles > num_customers:
        # Add dummy customers (columns)
        dummy_columns = np.zeros((num_vehicles, num_vehicles - num_customers))
        cost_matrix = np.hstack((cost_matrix, dummy_columns))
    elif num_customers > num_vehicles:
        # Add dummy vehicles (rows)
        dummy_rows = np.zeros((num_customers - num_vehicles, num_customers))
        cost_matrix = np.vstack((cost_matrix, dummy_rows))

    return cost_matrix
def optimize_allocation(vehicles, customers):
    cost_matrix = vehicles.calculate_cost_matrix(vehicles, customers)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    assignments = []
    for r, c in zip(row_ind, col_ind):
    # Exclude dummy assignments (columns or rows beyond actual customers or vehicles)
        if r < len(vehicles) and c < len(customers):
            assignments.append((r, c))

    return assignments



if __name__ == '__main__':

    test_case()
    # scenario = Scenario.initialize(
    #     scenario_id="scenario_1",
    #     start_time="2024-11-22T10:00:00",
    #     end_time="2024-11-22T12:00:00",
    #     num_vehicles=5,
    #     num_customers=10
    # )
    #
    # # Display the scenario
    # print(scenario)
    #
    # # Access vehicles and customers from the scenario object
    # vehicles = scenario.vehicles
    # customers = scenario.customers
    #
    # # Optimize the allocation of vehicles to customers
    # optimal_assignments = optimize_allocation(vehicles, customers)
    #
    # # Print the optimal assignments
    # for vehicle_idx, customer_idx in optimal_assignments:
    #     print(f"Vehicle {vehicles[vehicle_idx].id} is assigned to Customer {customers[customer_idx].id}")
