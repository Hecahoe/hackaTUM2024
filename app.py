from flask import Flask, request
import requests
import time

app = Flask(__name__)

be = "http://127.0.0.1:8080/"
runner = "http://127.0.0.1:8090/"

SIMULATION_SPEED = 0.1


@app.route("/create")
def create():
    vehicles = request.args.get("vehicles")
    customers = request.args.get("customers")
    params = {
        "numberOfVehicles": vehicles if vehicles else 5,
        "numberOfCustomers": customers if customers else 10,
    }
    response = requests.post(be + "scenario/create", params=params)
    return response.json()


@app.route("/")
def index():
    return "hello"


@app.route("/<scenarioid>")
def start(scenarioid):
    body = {"id": f"{scenarioid}"}
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
        return response.json()

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
        print("Initialized successfully")
    else:
        print(f"Problem initializing: {response.status_code}")
        return response.json()

    customers = get_customers(scenarioid)
    vehicles = get_vehicles(scenarioid)

    avail_custs = get_available_customers(customers)
    avail_vehics = get_available_vehicles(vehicles)

    # while len(avail_custs) != 0:
    update = []
    for c, v in zip(avail_custs, avail_vehics):
        update.append({"id": f"{v['id']}", "customerId": f"{c['id']}"})
    print("update")
    print(update)
    if len(update) != 0:
        response = requests.put(
            f"{runner}Scenarios/update_scenario/{scenarioid}",
            json={"vehicles": update},
        )
        print(response.json())

    avail_custs = get_available_customers(get_customers(scenarioid))
    avail_vehics = get_available_vehicles(get_vehicles(scenarioid))
    time.sleep(3)

    response = requests.get(f"{runner}Scenarios/get_scenario/{scenarioid}")
    return response.json()


def get_vehicles(scenarioid):
    return requests.get(f"{be}scenarios/{scenarioid}/vehicles").json()


def get_customers(scenarioid):
    return requests.get(f"{be}scenarios/{scenarioid}/customers").json()


def get_available_customers(customers):
    avail_custs = []
    for c in customers:
        if c["awaitingService"]:
            avail_custs.append(c)
    return avail_custs


def get_available_vehicles(vehicles):
    avail_vehics = []
    for v in vehicles:
        if v["isAvailable"]:
            avail_vehics.append(v)
    return avail_vehics


def customers_left(customers):
    for c in customers:
        if c["awaitingService"]:
            return True
    return False
