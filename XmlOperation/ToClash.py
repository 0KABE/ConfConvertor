import xml.etree.ElementTree as ET

import yaml

from XmlOperation.Snippet import AddSnippet

ProxyInfo = {
    "name": "name",
    "server": "server",
    "type": "type",
    "port": "port",
    "encrypt-method": "cipher",
    "password": "password",
    "obfs": "obfs",
    "obfs-host": "obfs-host",
}

ProxyGroupInfo = ["url", "interval"]


AllowBuiltIn = ["DIRECT", "REJECT"]
AllowRuleTag = ["DOMAIN-SUFFIX", "DOMAIN-KEYWORD",
                "DOMAIN", "IP-CIDR", "SOURCE-IP-CIDR", "GEOIP", "FINAL"]


def ToClash(root, snippet=None):
    Replace = {}
    conf = {"port": 7890,
            "socks-port": 7891,
            "allow-lan": False,
            "mode": "Rule",
            "log-level": "info",
            "external-controller": '0.0.0.0:9090',
            "secret": "",
            "Proxy": [],
            "Proxy Group": [],
            "Rule": []
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
                if attrib in elem.attrib:
                    if attrib == "type" and elem.get(attrib) == "custom":
                        value = "ss"
                    else:
                        value = elem.get(attrib)
                    dic[ProxyInfo[attrib]] = value
            conf["Proxy"].append(dic)

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
        conf["Proxy Group"].append(dic)
    for elem in root.find("Rule"):
        if elem.tag == "comment" or elem.tag not in AllowRuleTag:
            continue
        if elem.tag == "FINAL":
            l = "MATCH, "+elem.get("policy")
        else:
            l = elem.tag+", "+elem.get("match")+", "+elem.get("policy")
        conf["Rule"].append(l)

    return yaml.dump(conf)


if __name__ == "__main__":
    tree = ET.parse("Private_Demo.xml")
    root = tree.getroot()
    ToClash(root)
