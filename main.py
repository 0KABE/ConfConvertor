import xml.dom.minidom
import xml.etree.ElementTree as ET

import requests
from flask import make_response, request

from Clash.ToClash import ToClash
from Clash.TopologicalSort import TopologicalSort
from Expand.ExpandPolicyPath import ExpandPolicyPath
from Expand.ExpandRuleSet import ExpandRuleSet
from Surge3.ToSurge3 import ToSurge3
from Unite.CheckPolicyPath import NeedExpandPolicyPath
from Unite.GetProxyGroupType import GetProxyGroupType
from Unite.Surge3LikeConfig2XML import Content2XML
from Filter.GetList import FromConfig
from Filter.GetList import FromList


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
    result = "#!MANAGED-CONFIG https://api.OKAB3.com/surge3?url=" + url + \
        "&filename="+filename+"&interval="+interval+"&strict=" + \
        strict + " interval="+interval+" strict="+strict+"\n"
    x = Content2XML(content)
    x = ExpandPolicyPath(x)
    x = GetProxyGroupType(x)

    result += ToSurge3(x)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename="+filename
    return response


def Clash(request):
    url = request.args.get('url')
    filename = request.args.get("filename", "Config.yml")
    snippet = request.args.get("snippet")
    url_text = requests.get(url).content.decode()
    x = Content2XML(url_text)
    x = ExpandPolicyPath(x)
    x = ExpandRuleSet(x)
    x = TopologicalSort(x)

    result = ToClash(x, snippet)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename="+filename
    return response


def Filter(request):
    list_url = request.args.get("list")
    config_url = request.args.get("conf")
    regex = request.args.get("regex")
    if list_url:
        content = requests.get(list_url).content.decode()
        data = FromList(content, regex)
    if config_url:
        content = requests.get(config_url).content.decode()
        data = FromConfig(content, regex)
    response = make_response(data)
    response.headers["Content-Disposition"] = "attachment; filename="+"Filter.list"
    return response
