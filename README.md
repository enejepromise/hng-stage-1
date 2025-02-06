# Number Classification API

This is a simple API that takes a number as input and returns interesting mathematical properties about it, along with a fun fact from the [Numbers API](http://numbersapi.com/).

## Requirements

*   Python 3.6+
*   Flask
*   requests
*   flask_cors

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python3 -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install flask requests flask_cors
    ```

## Usage

1.  Run the application:

    ```bash
    python app.py
    ```

2.  Access the API endpoint:

    ```
    GET /api/classify-number?number=<number>
    ```

    Replace `<number>` with the integer you want to classify.  For example:

    ```
    GET /api/classify-number?number=371
    ```

## Example Responses

**Success (200 OK):**

```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}

## Error Handling
The API returns a 400 Bad Request error if the number parameter is missing or is not a valid integer. It also handles errors from the Numbers API gracefully, returning a generic fun fact message if the API is unavailable.

## Deployment
This API is hosted on a publicly accessible platform of your choice (Render). It supports CORS (Cross-Origin Resource Sharing), allowing access from different domains.
