import xml.etree.ElementTree as ET


def ProxyGroupTypeDict(root):
    dic = dict()
    for elem in root.find("Proxy"):
        dic[elem.get("name")] = elem.tag
    for elem in root.findall("ProxyGroup/policy"):
        dic[elem.get("name")] = elem.get("type")
    return dic


def GetProxyGroupType(root):
    dic = ProxyGroupTypeDict(root)
    for policy in root.findall("ProxyGroup/policy"):
        for elem in policy:
            elem.set("type", dic[elem.text])
    return root
