import requests
import numpy as np
from scipy.optimize import linear_sum_assignment

# API endpoints
SCENARIO_API = "http://localhost:8090"
BACKEND_API = "http://localhost:8080"

# Step 1: Create a scenario (assuming it's already done via frontend UI)
scenario_id = "8f599eca-7531-47b3-9268-2a221f8c66f4"  # Replace with actual scenario ID from the UI

# Step 2: Initialize the scenario
def initialize_scenario(scenario_id):
    response = requests.get(f"{SCENARIO_API}/Scenarios/get_scenario/{scenario_id}", json={"scenario_id": scenario_id})
    if response.status_code == 200:
        print("Scenario initialized successfully.")
    else:
        print("Failed to initialize scenario:", response.json())
        exit()

# Step 3: Run the scenario
def run_scenario(scenario_id, speed=0.2):
    response = requests.post(
        f"{SCENARIO_API}/Runner/launch_scenario/{scenario_id}",
        json={"scenario_id": scenario_id, "speed": speed}
    )
    print("Response status code:", response.status_code)
    print("Response text:", response.text)  # Log raw response
    if response.status_code == 200:
        print("Scenario running...")
    else:
        print("Failed to launch scenario:", response.text)  # Print raw text if JSON fails
        exit()


# Step 4: Get the current scenario state
def get_scenario_state(scenario_id):
    response = requests.get(f"{SCENARIO_API}/scenario/{scenario_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch scenario state:", response.json())
        return None

# Step 5: Assign vehicles to customers using Hungarian Algorithm
def assign_vehicles(state):
    vehicles = state["vehicles"]
    customers = state["customers"]

    vehicle_positions = np.array([[v["x"], v["y"]] for v in vehicles])
    customer_positions = np.array([[c["x"], c["y"]] for c in customers])

    # Calculate pairwise distances (Euclidean)
    distances = np.linalg.norm(
        vehicle_positions[:, None, :] - customer_positions[None, :, :], axis=2
    )

    # Apply Hungarian Algorithm for optimal assignment
    vehicle_indices, customer_indices = linear_sum_assignment(distances)

    assignments = [
        {"vehicle_id": vehicles[v]["id"], "customer_id": customers[c]["id"]}
        for v, c in zip(vehicle_indices, customer_indices)
    ]
    return assignments

# Step 6: Send assignments to the scenario runner
def update_scenario(assignments, scenario_id):
    response = requests.post(
        f"{SCENARIO_API}/scenarios/update_scenario",
        json={"scenario_id": scenario_id, "assignments": assignments}
    )
    if response.status_code == 200:
        print("Assignments updated.")
    else:
        print("Failed to update assignments:", response.json())

# Main Simulation Loop
def optimize_robotaxis(scenario_id):
    initialize_scenario(scenario_id)
    run_scenario(scenario_id)

    while True:
        # Get current scenario state
        state = get_scenario_state(scenario_id)
        if not state or state.get("status") == "finished":
            print("Simulation completed.")
            break

        # Assign vehicles to customers
        assignments = assign_vehicles(state)

        # Update the scenario with new assignments
        update_scenario(assignments, scenario_id)

# Run the optimizer
optimize_robotaxis(scenario_id)
