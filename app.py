'''
This a python flask API that takes a number and returns
interesting mathematical properties like
prime numbers, perfect numbers, Armstrong,
even and odd numbers and returns it in Json format.
It also handles CORS to ensure secured access across web pages

'''
from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
import requests

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

# Disable key sorting for Flask's JSON encoder
app.json.sort_keys = False


def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n):
    """Check if a number is perfect."""
    if n < 1:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n


def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    return sum(int(digit) ** power for digit in digits) == n


def digit_sum(n):
    """Calculate the sum of the digits of a number."""
    return sum(int(digit) for digit in str(abs(n)))


@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """
    Checks the mathematical properties of a number,
    and returns a JSON response containing the number,
    its properties, and a fun fact from the Numbers API.
    """
    number = request.args.get('number')

    if not number:
        return jsonify({"error": "Number parameter is required"}), 400

    try:
        number = int(number)  # Convert to integer
    except ValueError:
        return jsonify({"error": "Invalid number"}), 400

    # Check mathematical properties
    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    sum_digits = digit_sum(number)
    parity = "odd" if number % 2 != 0 else "even"

    properties = ["armstrong"] if armstrong else []
    properties.append(parity)

    # Fetch fun fact from the Numbers API
    api_url = f"http://numbersapi.com/{number}/math?json"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        fun_fact = response.json().get("text", "")
    except requests.RequestException:
        fun_fact = "Fun fact could not be retrieved."

    # Build response
    data = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": sum_digits,
        "fun_fact": fun_fact
    }
    return jsonify(data), 200


@app.errorhandler(404)
def page_not_found(e):
    """Return an error message in JSON for undefined routes."""
    return jsonify({"error": "Route not found"}), 404


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))  # Default to 5000 if not provided
    app.run(host="0.0.0.0", port=port, debug=True)  # Listen on all interfaces (0.0.0.0)