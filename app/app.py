from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/metrics")
def metrics():
    return jsonify({"orders_processed": random.randint(1, 100)}), 200

@app.route("/orders")
def orders():
    return jsonify({"message": "Order placed successfully!"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
