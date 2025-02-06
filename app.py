'''
This a python flask API that takes a number and returns
interesting mathematical properties like
prime numbers, perfect numbers, Armstrong,
even and odd numbers and returns it in Json format.
It also handles CORS to ensure secured access across web pages

'''
from flask import Flask, jsonify, request
import requests
import math
from flask_cors import CORS
from os import environ


#Initializing app
app = Flask(__name__)
# Enabling Cross Origin Recourse Sharing
CORS(app)

app.json.sort_keys = False

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(2, n ** 5)+ 1):
        if i % 2 == 0:
            return False
    return True

def is_perfect(n):
    '''
    A function that check if a number is perfect
    '''
    if n < 1:
        return False
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    return sum(int(digit)  ** power for digit in digits) == n

def digit_sum(n):
    '''
    A function to calculate the sum of the digits of a number.
    '''
    return sum(int(digit) for digit in str(abs(n)))

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    '''
    This checks the mathematical properties of a number,
    and returns a JSON response containing the number,
    its properties, and a fun fact about the number
    from the Numbers API.
    '''
    # Getting the number parameter
    number = request.args.get('number')

    if not number:  
        data = {
            "number": "alphabet",
            "error": True  
        }
        return jsonify(data), 400

    try:
        number = int(number)
    except ValueError:
        return jsonify({
            "number": "alphabet",
            "error": True}
        ), 400

    prime = is_prime(number)
    perfect = is_perfect(number)
    armstrong = is_armstrong(number)
    sum_digits = digit_sum(number)
    parity = "odd" if number % 2 != 0 else "even"
   
    properties = []
    if armstrong:
        properties.append("armstrong")
    properties.append(parity)

    # Fetch the fun fact from the Numbers API using the math endpoint
    api_url = f"http://numbersapi.com/{number}/math?json"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        # print(data)
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
    return jsonify(data), 200  

# Errors handling and redirections
@app.errorhandler(404)
def page_not_found(e):
    '''
    Returns an error message in JSON
    when the user tries to access
    a invalid or undefined route.
    '''
    # return redirect('/')
    data = {
        "number": "alphabet",
        "error": True  
    }
    return jsonify(data), 404




if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))   
    app.run(host="0.0.0.0", port=port, debug=True) 