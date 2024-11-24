from flask import Flask, request
import requests
import time

from Customer import init_customers
from Vehicle import init_vehicles
from fleetmanager import Fleetmanager

app = Flask(__name__)

be = "http://127.0.0.1:8080/"
runner = "http://127.0.0.1:8090/"

SIMULATION_SPEED = 0.01
scenarioid = None
fleetmanager = Fleetmanager(None, None)


@app.route("/")
def index():
    return "hello"


@app.route("/initialize")
def initialize():
    global fleetmanager

    vehicles = request.args.get("vehicles")
    customers = request.args.get("customers")
    params = {
        "numberOfVehicles": vehicles if vehicles else 5,
        "numberOfCustomers": customers if customers else 10,
    }
    response = requests.post(be + "scenario/create", params=params)
    scenarioid = response.json()["id"]

    initialize_scenario(scenarioid)

    launch_scenario(scenarioid)

    scenario = get_scenario(scenarioid)
    customer_objects = init_customers(scenario["customers"])
    vehicles_objects = init_vehicles(scenario["vehicles"])

    fleetmanager = Fleetmanager(customer_objects, vehicles_objects)

    return scenario


@app.route("/update")
def start():
    waiting_customers = fleetmanager.get_waiting_customers()

    update_response = []
    if len(waiting_customers) != 0:
        updates = fleetmanager.get_updates()
        for u in updates:
            vehicle = fleetmanager.get_vehicles()[u[0]]
            customer = fleetmanager.get_customers()[u[1]]
            update_response.append(
                {
                    "vehicleX": vehicle.coordX,
                    "vehicleY": vehicle.coordY,
                    "customerX": customer.coordX,
                    "customerY": customer.coordY,
                    "destinationX": customer.destinationX,
                    "destinationY": customer.destinationY,
                    "remainingTravelTime": vehicle.remainingTravelTime,
                }
            )
        if len(updates) != 0:
            response = update_scenario(scenarioid, updates)
            print("Update")
        else:
            print("No update")
        time.sleep(10 * SIMULATION_SPEED)

        scenario = get_scenario(scenarioid)
        fleetmanager.set_customers(init_customers(scenario["customers"]))
        fleetmanager.set_vehicles(init_customers(scenario["vehicles"]))

        waiting_customers = fleetmanager.get_waiting_customers()
        print(f"Waiting customers {len(waiting_customers)}")

    finished_customers = [
        c.id for c in fleetmanager.get_customers().values() if not c.awaitingService
    ]
    return {"finisched_customers": finished_customers, "updates": update_response}


def update_scenario(scenarioid, updates):
    json = {"vehicles": [{"id": u[0], "customerId": u[1]} for u in updates]}
    print(f"updated: {json}")
    response = requests.put(
        f"{runner}Scenarios/update_scenario/{scenarioid}",
        json=json,
    )
    if response.status_code == 200:
        print("Update successful")
        return response
    else:
        print("Update failed")
        exit()


def initialize_scenario(scenarioid):
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    params = {"db_scenario_id": scenarioid}
    response = requests.post(
        f"{runner}Scenarios/initialize_scenario",
        json={},
        headers=headers,
        params=params,
    )
    if response.status_code == 200:
        print("Initialized successfully")
    else:
        print(f"Problem initializing: {response.status_code}")


def launch_scenario(scenarioid):
    body = {"id": f"{scenarioid}"}
    speed = request.args.get("speed")
    response = requests.post(
        f"{runner}Runner/launch_scenario/{scenarioid}",
        json=body,
        params={
            "speed": speed if speed else SIMULATION_SPEED,
            "accept": "application/json",
        },
    )
    if response.status_code == 200:
        print("Launched successfully")
    else:
        print(f"Problem launching: {response.status_code}")


def get_vehicles(scenarioid):
    return requests.get(f"{runner}Scenarios/get_scenario/{scenarioid}").json()[
        "vehicles"
    ]


def get_scenario(scenarioid):
    return requests.get(f"{runner}Scenarios/get_scenario/{scenarioid}").json()


def get_customers(scenarioid):
    return requests.get(f"{runner}Scenarios/get_scenario/{scenarioid}").json()[
        "customers"
    ]
