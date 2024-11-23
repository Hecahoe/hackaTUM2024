import math
import time
from typing import List

import numpy as np
from scipy.optimize import linear_sum_assignment

import Customer
import Vehicle


class Runner:
    def __init__(self, vehicles: List[Vehicle], customers: List[Customer]):
        self.vehicles = vehicles
        self.customers = customers
        self.time_elapsed = 0  # Track elapsed simulation time (in minutes)
        initialiseHashMap(customers)

    customerHasArrived = {}

    def simulate(self):
        """
        Runs the simulation until all customers have arrived at their destinations.
        """
        while not all(customer.arrivedAtDestination for customer in self.customers):
            print(f"\n--- Time: {self.time_elapsed} minutes ---")
            # Re-calculate optimal assignments
            assignments = optimize_allocation(self.vehicles, self.customers)

            # Assign vehicles to customers
            self.assign_vehicles(assignments)

            # Simulate one minute of travel
            self.update_positions()

            # Increment time
            self.time_elapsed += 1

        print("\nAll customers have arrived at their destinations!")
        print(f"Total simulation time: {self.time_elapsed} minutes.")

    def assign_vehicles(self, assignments):
        """
        Assigns vehicles to customers based on the given assignments.

        Parameters:
            assignments (List[Tuple[int, int]]): Optimal (vehicle index, customer index) assignments.
        """
        for vehicle_idx, customer_idx in assignments:
            vehicle = self.vehicles[vehicle_idx]
            customer = self.customers[customer_idx]

            # Skip customers who have already arrived
            if customer.arrivedAtDestination:
                continue

            # Assign vehicle to customer
            vehicle.customerId = customer.id
            vehicle.remainingTravelTime = self.calculate_travel_time(vehicle, customer)
            print(f"Vehicle {vehicle.id} is assigned to Customer {customer.id}.")

    def calculate_travel_time(self, vehicle: Vehicle, customer: Customer) -> float:
        """
        Calculates the travel time for a vehicle to reach its assigned customer.

        Parameters:
            vehicle (Vehicle): The vehicle.
            customer (Customer): The customer.

        Returns:
            float: Travel time in minutes.
        """
        distance = math.sqrt(
            (vehicle.coordX - customer.coordX) ** 2 + (vehicle.coordY - customer.coordY) ** 2
        )
        travel_time = (distance / vehicle.vehicleSpeed) * 60  # Convert hours to minutes
        return travel_time

    def update_positions(self):
        """
        Updates the positions of vehicles and checks if customers have arrived.
        """
        for vehicle in self.vehicles:
            if vehicle.customerId is None or vehicle.remainingTravelTime <= 0:
                continue  # Skip vehicles not assigned to customers

            # Move vehicle towards the customer
            vehicle.remainingTravelTime -= 1  # Simulate one minute of travel
            if vehicle.remainingTravelTime <= 0:
                # Vehicle has reached the customer
                customer = next(
                    c for c in self.customers if c.id == vehicle.customerId
                )
                customer.arrivedAtDestination = True
                vehicle.customerId = None
                print(f"Customer {customer.id} has arrived at their destination.")


def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_cost_matrix(vehicles, customers):
    num_vehicles = len(vehicles)
    num_customers = len(customers)
    # Initialize cost matrix with distances
    cost_matrix = np.zeros((num_vehicles, num_customers))
    for i, vehicle in enumerate(vehicles):
        for j, customer in enumerate(customers):
            cost_matrix[i, j] = (
                vehicles.calculate_distance(vehicle.coordX, vehicle.coordY, customer.coordX, customer.coordY))

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



def initialiseHashMap(customers: List[Customer]):
    for customer in customers:
        Runner.customerHasArrived[customer] = False
