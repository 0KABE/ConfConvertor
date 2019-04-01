import requests
from flask import request
from flask import make_response
from Surge3LikeConfig2XML import Content2XML
from XML2Surge3 import XML2Surge3


def Surge3Expand(request):
    url = request.args.get('url')
    req = requests.get(url)
    content = req.content.decode()
    # content = bytes.decode(content)
    x = Content2XML(content)
    result = XML2Surge3(x)
    response = make_response(result)
    # response = make_response(Surge3ToClash(content))
    response.headers["Content-Disposition"] = "attachment; filename=config.conf"
    return response
