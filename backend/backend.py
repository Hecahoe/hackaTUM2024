import math

from flask import Flask, jsonify
import random

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# In-memory data storage with Munich coordinates
data = {
    "cars": [
        {"id": 1, "position": [48.1351, 11.5820]},  # Example car positions in Munich
        {"id": 2, "position": [48.1486, 11.5736]},
    ],
    "customers": [
        {"id": 1, "start": [48.137154, 11.576124], "end": [48.155166, 11.601437]},
        {"id": 2, "start": [48.131887, 11.549703], "end": [48.126472, 11.582037]},
    ],
    "finished_customers": [],
    "new_routes": []
}


@app.route('/initialize', methods=['GET'])
def initialize():
    """
    Initialize and return the cars with their positions and customers with start/end points.
    """
    # "cars": data["cars"],
    return jsonify({
        "cars": data["cars"],
        "customers": data["customers"]
    })


@app.route('/update', methods=['GET'])
def update():
    """
    Update endpoint: randomly returns either finished customers or new routes.
    """
    if random.randrange(0, 100) > 80:
        return []
    # Randomly decide to return finished customers or new routes
    choice = random.choice(["finished", "new_routes"])


    if choice == "finished":
        # Simulate finished customers by moving them to "finished_customers" list
        if data["customers"]:
            finished_customer = data["customers"].pop(0)
            data["finished_customers"].append(finished_customer)
            return jsonify({
                "type": "finished_customers",
                "data": [finished_customer]
            })
        else:
            return jsonify({
                "type": "finished_customers",
                "data": []  # No customers left to finish
            })

    elif choice == "new_routes":
        # Generate a new route for a random car
        if data["cars"]:
            car = data["cars"].pop(0)
            new_route = {
                "car_id": car["id"],
                "start": [car["position"][0], car["position"][1]],
                "end": [random.uniform(48.1000, 48.2000), random.uniform(11.5000, 11.6500)]
            }
            data["new_routes"].append(new_route)
            return jsonify({
                "type": "new_routes",
                "data": [new_route]
            })
        else:
            return jsonify({
                "type": "new_routes",
                "data": []  # No cars to assign new routes
            })


if __name__ == '__main__':
    app.run(debug=True)
