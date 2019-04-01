import requests
from flask import make_response, request

import ConfigOperation.GetUrlContent
import ConfigOperation.Surge3LikeConfig2XML
import ConfigOperation.XML2Surge3
from ConfigOperation.Surge3LikeConfig2XML import Content2XML
from ConfigOperation.XML2Surge3 import XML2Surge3


def Surge3Expand(request):
    url = request.args.get('url')
    filename = request.args.get("filename", "Config.conf")
    content = requests.get(url).text
    x = Content2XML(content)
    result = XML2Surge3(x)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename="+filename
    return response
