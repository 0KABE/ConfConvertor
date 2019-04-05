import xml.etree.ElementTree as ET
import yaml

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

Replace = {}


def ToClash(root):
    for elem in root.find("Proxy"):
        if elem.tag == "Built-in":
            Replace[elem.get("name")] = elem.get("policy")
        else:
            dic = {}
            for attrib in ProxyInfo:
                if attrib in elem.attrib:
                    dic[ProxyInfo[attrib]] = elem.get(attrib)
            conf["Proxy"].append(dic)

    for elem in root.findall("ProxyGroup/policy"):
        dic = {}
        dic["name"] = elem.get("name")
        dic["type"] = elem.get("type")
        proxies = []
        for it in elem:
            if it.text in Replace:
                proxies.append(Replace[it.text])
            else:
                proxies.append(it.text)
        dic["proxies"] = proxies
        dic["url"] = elem.get("url", "http://www.gstatic.com/generate_204")
        dic["interval"] = elem.get("interval", "600")
        conf["Proxy Group"].append(dic)
    for elem in root.find("Rule"):
        if elem.tag == "comment":
            continue
        if elem.tag == "FINAL":
            l = "MATCH, "+elem.get("policy")
        else:
            l = elem.tag+", "+elem.get("match")+", "+elem.get("policy")
        conf["Rule"].append(l)

    print("Hello World")
    f = open("Conf.yml", "w")
    yaml.dump(conf, f)
    return conf


if __name__ == "__main__":
    tree = ET.parse("Private_Demo.xml")
    root = tree.getroot()
    ToClash(root)
