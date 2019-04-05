import xml.dom.minidom
import xml.etree.ElementTree as ET

import requests
from flask import make_response, request

from Expand.ExpandPolicyPath import ExpandPolicyPath
from Expand.ExpandRuleSet import ExpandRuleSet
from XmlOperation.CheckPolicyPath import NeedExpandPolicyPath
from XmlOperation.Surge3LikeConfig2XML import Content2XML
from XmlOperation.ToClash import ToClash
from XmlOperation.TopologicalSort import TopologicalSort
from XmlOperation.ToSurge3 import ToSurge3


def Surge3(request):
    """
    Args:
        request (flask.Request): HTTP request object.
    Return:
        A Surge3Pro-support configuration
    Do:
        Get 2 parameters: url & filename
        url: the url of the remote file
        filename: the file name of the configuration will be returned, default(no filename parameter in request) to Config.conf

        Function ExpandPolicyPath will be excuted only when 'Proxy Group' illegal format be exist
        Illegal format: a 'Proxy Group' only allow one policy when there is a policy-path
    """
    url = request.args.get('url')
    filename = request.args.get("filename", "Config.conf")
    interval = request.args.get("interval", "86400")
    strict = request.args.get("strict", "false")
    content = requests.get(url).text
    result = "#!MANAGED-CONFIG https://asia-east2-trans-filament-233005.cloudfunctions.net/surge3?url=" + url + \
        "&filename="+filename+"&interval="+interval+"&strict=" + \
        strict + " interval="+interval+" strict="+strict+"\n"
    x = Content2XML(content)
    if NeedExpandPolicyPath(x):
        x = ExpandPolicyPath(x)

    result += ToSurge3(x)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename="+filename
    return response


def Clash(request):
    url = request.args.get('url')
    filename = request.args.get("filename", "Config.yml")
    content = requests.get(url).text
    x = Content2XML(content)
    x = ExpandPolicyPath(x)
    x = ExpandRuleSet(x)
    x = TopologicalSort(x)

    result = ToClash(x)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename="+filename
    return response
