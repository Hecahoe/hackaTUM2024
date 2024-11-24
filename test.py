import requests

SCENARIO_API = "http://localhost:8090"
RUNNER_API = "http://localhost:8080"
print(requests.post(
        f"{SCENARIO_API}/Scenarios/initialize_scenario",
        json={ "speed": 0.2, "scenario_id": "f6a9c0d1-fc78-4bdc-bb75-12ba8904757c"}).content)

print(requests.post(
        f"{RUNNER_API}/Runner/launch_scenario/f6a9c0d1-fc78-4bdc-bb75-12ba8904757c",
        json={ "speed": 0.2}))