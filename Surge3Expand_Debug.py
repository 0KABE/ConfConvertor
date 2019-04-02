import re

import requests
from flask import Flask, Response, make_response, request

import XmlOperation.GetUrlContent
import XmlOperation.Surge3LikeConfig2XML
import XmlOperation.XML2Surge3
from main import Surge3

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
    response = Surge3(request)
    return response


if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)
