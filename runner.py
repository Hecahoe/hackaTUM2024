import math
import time
from typing import List

import numpy as np
from scipy.optimize import linear_sum_assignment

import Customer
import Vehicle

class Runner:

    def __init__(self, number_of_vehicles: int, number_of_customers: int):



    happyCustomers = {} #contains the id of customers that have been transported or are currently transported

















def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_travel_time(vehicle, future_costomer):
    travel_time = 0
    vehicle_x = vehicle.coordX
    vehicle_y = vehicle.coordY
    current_speed = vehicle.vehicleSpeed

    if not vehicle.isAvailable:
        current_customer = vehicle.customers[
            future_costomer.customer_id]  # This will be a pull request "/customers/{customerId}"
        travel_time += calculate_distance(vehicle_x, vehicle_y, current_customer.destinationX,
                                          current_customer.destinationY) / current_speed
        travel_time += calculate_distance(current_customer.destinationX, current_customer.destinationY,
                                          future_costomer.coordX, future_costomer.coordY) / current_speed
    else:
        customer_x = future_costomer.coordX
        customer_y = future_costomer.coordY
        travel_time += calculate_distance(vehicle_x, vehicle_y, customer_x, customer_y) / current_speed

    return travel_time


def calculate_cost_matrix(vehicles, customers):
    # filter customers that awaitingService == False

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
