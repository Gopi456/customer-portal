from flask import Flask, request, jsonify

app = Flask(__name__)

customers = []
next_id = 1


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "application": "Customer Portal"
    }), 200


@app.route("/customers", methods=["POST"])
def create_customer():
    global next_id

    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({
            "error": "Name and email are required"
        }), 400

    customer = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"]
    }

    customers.append(customer)
    next_id += 1

    return jsonify(customer), 201


@app.route("/customers", methods=["GET"])
def get_customers():
    return jsonify(customers), 200


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):

    for customer in customers:
        if customer["id"] == customer_id:
            return jsonify(customer), 200

    return jsonify({
        "error": "Customer not found"
    }), 404


if __name__ == "__main__":
    print("Starting Customer Portal")
    app.run(host="0.0.0.0", port=8080)