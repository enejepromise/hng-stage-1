'''
This is a python flask API that takes a number and returns
interesting mathematical properties like
prime numbers, perfect numbers, Armstrong,
even and odd numbers and returns it in Json format.
It also handles CORS to ensure secured access across web pages

'''
from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
import requests

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross Origin Resource Sharing (CORS)

# Disable key sorting for Flask's JSON encoder (as requested in requirements)
app.json.sort_keys = False

def is_prime(n):
    """
    A function to check if a number is prime.
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    """
    A function to check if a number is perfect.
    """
    if n < 1:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    """
    A function to check if a number is an Armstrong number.
    """
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    return sum(int(digit) ** power for digit in digits) == n

def digit_sum(n):
    """
    A function to calculate the sum of the digits of a number.
    """
    return sum(int(digit) for digit in str(n))
@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """
    Checks the mathematical properties of a number,
    and returns a JSON response containing the number,
    its properties, and a fun fact about the number
    from the Numbers API.
    """
    # Get the number parameter from the query string
    number = request.args.get('number')

    # Validate the number input
    if not number:
        return jsonify({"number": "alphabet", "error": True}), 400

    try:
        number = int(number)
    except ValueError:
        return jsonify({"number": number, "error": True}), 400

    # Initialize common fields
    prime = is_prime(number)
    perfect = is_perfect(number)
    sum_digits = digit_sum(abs(number))  # Compute digit sum using absolute value
    parity = "odd" if abs(number) % 2 != 0 else "even"
    
    # Generate properties list
    properties = ["negative"] if number < 0 else []
    properties.append(parity)

    # Handle negative numbers: No fun facts available
    if number < 0:
        fun_fact = "Fun facts are only available for non-negative numbers."
    else:
        # Fetch the fun fact from the Numbers API using the math endpoint
        api_url = f"http://numbersapi.com/{number}/math?json"
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            fun_fact = data.get("text", "")
        except Exception as e:
            fun_fact = f"Could not retrieve fun fact: {str(e)}"

    # Build the JSON response
    data = {
        "number": number,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": sum_digits,
        "fun_fact": fun_fact
    }
    return jsonify(data), 200  # Return the JSON response with status 200


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))  # Default to 5000 if not provided
    app.run(host="0.0.0.0", port=port, debug=True)  # Listen on all interfaces (0.0.0.0) and use the specified port
