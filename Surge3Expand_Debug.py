from flask import Flask
from flask import request
from flask import Response
from flask import make_response
import requests
import re
import ConfigOperation.GetUrlContent
import ConfigOperation.XML2Surge3
import ConfigOperation.Surge3LikeConfig2XML
from main import Surge3Expand

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
# Cloud Function: def main(request):
# Local debug: def main():
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
    # url = request.args.get('url')
    # req = requests.get(url)
    # content = req.content.decode()
    # # content = bytes.decode(content)
    # x = Content2XML(content)
    # result = XML2Surge3(x)
    # response = make_response(result)
    # # response = make_response(Surge3ToClash(content))
    # response.headers["Content-Disposition"] = "attachment; filename=config.conf"
    response=Surge3Expand(request)
    return response


# Code for debug locally, do not sync to the cloud function platform
if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)
