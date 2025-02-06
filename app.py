'''
This a python flask API that takes a number and returns
interesting mathematical properties like
prime numbers, perfect numbers, Armstrong,
even and odd numbers and returns it in Json format.
It also handles CORS to ensure secured access across web pages

'''
from flask import Flask, request, jsonify
import math
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def is_perfect(n):
    """Check if a number is perfect."""
    if n <= 1:
        return False
    sum_divisors = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            sum_divisors += i
            if i * i != n:
                sum_divisors += n // i
    return sum_divisors == n


def is_armstrong(n):
    """Check if a number is an Armstrong number."""
    num_str = str(n)
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit) ** num_digits for digit in num_str)
    return sum_of_powers == n


def get_digit_sum(n):
    """Calculate the sum of the digits of a number."""
    return sum(int(digit) for digit in str(n))


def get_fun_fact(number):
    """Get a fun fact from the Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math")
        response.raise_for_status()  
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fun fact from Numbers API: {e}")
        return "Could not retrieve a fun fact at this time."


@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Classify a number and return its properties and a fun fact."""
    try:
        number = request.args.get('number')
        if not number:
            return jsonify({"error": True, "message": "Missing number parameter"}), 400

        number = int(number)  # Convert to integer

    except ValueError:
        return jsonify({"number": request.args.get('number'), "error": True}), 400

    is_prime_num = is_prime(number)
    is_perfect_num = is_perfect(number)
    is_armstrong_num = is_armstrong(number)

    properties = []
    if is_armstrong_num:
        properties.append("armstrong")
    if number % 2 == 0:
        if "armstrong" not in properties:
            properties.append("even")
        else:
            properties.append("even")
    else:
        if "armstrong" not in properties:
            properties.append("odd")
        else:
            properties.append("odd")

    digit_sum = get_digit_sum(number)
    fun_fact = get_fun_fact(number)

    response = {
        "number": number,
        "is_prime": is_prime_num,
        "is_perfect": is_perfect_num,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return jsonify(response), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  
    app.run(debug=True, host='0.0.0.0', port=port) 
