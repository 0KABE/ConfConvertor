import requests
from flask import Flask, Response, make_response, request
from main import Filter

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        #flask.Flask.make_response>`.
        `make_response <http://flask.pocoo.org/docs/1.0/api/
    """
    response = Filter(request)
    return response


if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)
