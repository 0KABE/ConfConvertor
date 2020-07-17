import xml.etree.ElementTree as ET

import yaml

from . import Snippet
from .Snippet import AddSnippet

ProxyInfo = {
    "name": "name",
    "server": "server",
    "type": "type",
    "port": "port",
    "encrypt-method": "cipher",
    "password": "password",
    "obfs": "plugin",
    "obfs-host": "plugin-opts",
    "udp-relay": "udp"
}

ProxyGroupInfo = ["url", "interval"]


AllowBuiltIn = ["DIRECT", "REJECT"]
AllowRuleTag = ["DOMAIN-SUFFIX", "DOMAIN-KEYWORD",
                "DOMAIN", "IP-CIDR", "SRC-IP-CIDR", "GEOIP", "FINAL"]


def ToClashV1(root, snippet=None):
    Replace = {}
    conf = {"port": 7890,
            "socks-port": 7891,
            "allow-lan": False,
            "mode": "Rule",
            "log-level": "info",
            "external-controller": '0.0.0.0:9090',
            "secret": "",
            "proxies": [],
            "proxy-groups": [],
            "rules": []
            }

    # add snippet
    if snippet:
        conf = AddSnippet(snippet, conf)

    for elem in root.find("Proxy"):
        if elem.tag == "Built-in":
            Replace[elem.get("name")] = elem.get("policy").upper()
        else:
            dic = {}
            for attrib in ProxyInfo:
                if attrib == "obfs" and attrib in elem.attrib:
                    dic["plugin"] = "obfs"
                    if "plugin-opts" not in dic:
                        dic["plugin-opts"] = {}
                    dic["plugin-opts"]["mode"] = elem.get(attrib)
                if attrib == "obfs-host" and attrib in elem.attrib:
                    if "plugin-opts" not in dic:
                        dic["plugin-opts"] = {}
                    dic["plugin-opts"]["host"] = elem.get(attrib)
                elif attrib in elem.attrib:
                    if attrib == "type" and elem.get(attrib) == "custom":
                        value = "ss"
                    else:
                        if(elem.get(attrib) == "true"):
                            value = True
                        elif(elem.get(attrib) == "false"):
                            value = False
                        else:
                            value = elem.get(attrib)
                    dic[ProxyInfo[attrib]] = value
            conf["proxies"].append(dic)

    for elem in root.findall("ProxyGroup/policy"):
        dic = {}
        dic["name"] = elem.get("name")
        dic["type"] = elem.get("type")
        proxies = []
        for it in elem:
            if it.text in Replace:
                if Replace[it.text] in AllowBuiltIn:
                    proxies.append(Replace[it.text])
            else:
                proxies.append(it.text)
        dic["proxies"] = proxies
        if elem.get("type") != "select":
            dic["url"] = elem.get("url", "http://www.gstatic.com/generate_204")
            dic["interval"] = elem.get("interval", "600")
        conf["proxy-groups"].append(dic)
    for elem in root.find("Rule"):
        if elem.tag == "comment" or elem.tag not in AllowRuleTag:
            continue
        if elem.tag == "FINAL":
            l = "MATCH, "+elem.get("policy")
        else:
            l = elem.tag+", "+elem.get("match")+", "+elem.get("policy")
        conf["rules"].append(l)

    return yaml.dump(conf)
